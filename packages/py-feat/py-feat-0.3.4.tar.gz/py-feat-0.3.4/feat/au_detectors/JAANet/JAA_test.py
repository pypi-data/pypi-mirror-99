import cv2
import numpy as np
import pandas as pd
import torch
import math
import pandas as pd
import numpy as np
import feat.au_detectors.JAANet.JAANet_model as network
import torch.nn as nn
from PIL import Image
from torchvision import transforms
from feat.utils import get_resource_path, convert68to49
import os


class JAANet(nn.Module):
    def __init__(self) -> None:
        """
        Initialize.
        Args:
            img_data: numpy array image data files of shape (N,3,W,H)
            land_data: numpy array landmark data of shape (N, 49*2)
        """
        # self.imgs = img_data
        # self.land_data = land_data
        super(JAANet,self).__init__()
        
        self.params = {
            "config_unit_dim": 8,
            "config_crop_size": 176,
            "config_map_size": 44,
            "config_au_num": 12,
            "config_land_num": 49,
            "config_fill_coeff": 0.56,
            "config_write_path_prefix": get_resource_path(),
        }
        
        config_unit_dim = self.params["config_unit_dim"]
        config_crop_size = self.params["config_crop_size"]
        config_map_size = self.params["config_map_size"]
        config_au_num = self.params["config_au_num"]
        config_land_num = self.params["config_land_num"]
        config_fill_coeff = self.params["config_fill_coeff"]
        config_write_path_prefix = self.params["config_write_path_prefix"]

        self.region_learning = network.network_dict["HMRegionLearning"](
            input_dim=3, unit_dim=config_unit_dim
        )
        self.align_net = network.network_dict["AlignNet"](
            crop_size=config_crop_size,
            map_size=config_map_size,
            au_num=config_au_num,
            land_num=config_land_num,
            input_dim=config_unit_dim * 8,
            fill_coeff=config_fill_coeff,
        )
        self.local_attention_refine = network.network_dict["LocalAttentionRefine"](
            au_num=config_au_num, unit_dim=config_unit_dim
        )
        self.local_au_net = network.network_dict["LocalAUNetv2"](
            au_num=config_au_num,
            input_dim=config_unit_dim * 8,
            unit_dim=config_unit_dim,
        )
        self.global_au_feat = network.network_dict["HLFeatExtractor"](
            input_dim=config_unit_dim * 8, unit_dim=config_unit_dim
        )
        self.au_net = network.network_dict["AUNet"](
            au_num=config_au_num, input_dim=12000, unit_dim=config_unit_dim
        )
        
        self.use_gpu = torch.cuda.is_available()


        if self.use_gpu:
            self.region_learning = self.region_learning.cuda()
            self.align_net = self.align_net.cuda()
            self.local_attention_refine = self.local_attention_refine.cuda()
            self.local_au_net = self.local_au_net.cuda()
            self.global_au_feat = self.global_au_feat.cuda()
            self.au_net = self.au_net.cuda()
            # Load parameters
            # load_map = 'cpu' if True else 'false'
            # au_occur_model_path = os.path.join(
            #     config_write_path_prefix , '/region_learning' , '.pth')
            # print("should load data at ",os.path.join(config_write_path_prefix , 'region_learning.pth'))
            # print("Directory Files:")
            # print(os.listdir(config_write_path_prefix))
            self.region_learning.load_state_dict(
                torch.load(
                    os.path.join(config_write_path_prefix, "region_learning.pth")
                )
            )
            self.align_net.load_state_dict(
                torch.load(os.path.join(config_write_path_prefix, "align_net.pth"))
            )
            self.local_attention_refine.load_state_dict(
                torch.load(
                    os.path.join(config_write_path_prefix, "local_attention_refine.pth")
                )
            )
            self.local_au_net.load_state_dict(
                torch.load(os.path.join(config_write_path_prefix, "local_au_net.pth"))
            )
            self.global_au_feat.load_state_dict(
                torch.load(os.path.join(config_write_path_prefix, "global_au_feat.pth"))
            )
            self.au_net.load_state_dict(
                torch.load(os.path.join(config_write_path_prefix, "au_net.pth"))
            )
        else:
            self.region_learning.load_state_dict(
                torch.load(
                    os.path.join(config_write_path_prefix, "region_learning.pth"),
                    map_location={"cuda:0": "cpu"},
                )
            )
            self.align_net.load_state_dict(
                torch.load(
                    os.path.join(config_write_path_prefix, "align_net.pth"),
                    map_location={"cuda:0": "cpu"},
                )
            )
            self.local_attention_refine.load_state_dict(
                torch.load(
                    os.path.join(
                        config_write_path_prefix, "local_attention_refine.pth"
                    ),
                    map_location={"cuda:0": "cpu"},
                )
            )
            self.local_au_net.load_state_dict(
                torch.load(
                    os.path.join(config_write_path_prefix, "local_au_net.pth"),
                    map_location={"cuda:0": "cpu"},
                )
            )
            self.global_au_feat.load_state_dict(
                torch.load(
                    os.path.join(config_write_path_prefix, "global_au_feat.pth"),
                    map_location={"cuda:0": "cpu"},
                )
            )
            self.au_net.load_state_dict(
                torch.load(
                    os.path.join(config_write_path_prefix, "au_net.pth"),
                    map_location={"cuda:0": "cpu"},
                )
            )

        self.region_learning.eval()
        self.align_net.eval()
        self.local_attention_refine.eval()
        self.local_au_net.eval()
        self.global_au_feat.eval()
        self.au_net.eval()


    def align_face_49pts(self, img, img_land, box_enlarge=2.9, img_size=200):
        """
        code from:
        https://github.com/ZhiwenShao/PyTorch-JAANet/blob/master/dataset/face_transform.py
        Did some small modifications to fit into our program.
        The function performs preproecessing transformations on pictures.
        Args:
            img: iamges loaded by cv2. Shape: (3,H,W)
            img_land: landmark file for the img. Shape()
            box_enlarge: englarge factor for the face transform, centered at face
            img_size: size of the desired output image
        Return:
            aligned_img: aligned images by cv2
            new_land: transformed landmarks
            biocular: biocular distancxe
        """
        leftEye0 = (
            img_land[2 * 19]
            + img_land[2 * 20]
            + img_land[2 * 21]
            + img_land[2 * 22]
            + img_land[2 * 23]
            + img_land[2 * 24]
        ) / 6.0
        leftEye1 = (
            img_land[2 * 19 + 1]
            + img_land[2 * 20 + 1]
            + img_land[2 * 21 + 1]
            + img_land[2 * 22 + 1]
            + img_land[2 * 23 + 1]
            + img_land[2 * 24 + 1]
        ) / 6.0
        rightEye0 = (
            img_land[2 * 25]
            + img_land[2 * 26]
            + img_land[2 * 27]
            + img_land[2 * 28]
            + img_land[2 * 29]
            + img_land[2 * 30]
        ) / 6.0
        rightEye1 = (
            img_land[2 * 25 + 1]
            + img_land[2 * 26 + 1]
            + img_land[2 * 27 + 1]
            + img_land[2 * 28 + 1]
            + img_land[2 * 29 + 1]
            + img_land[2 * 30 + 1]
        ) / 6.0
        deltaX = rightEye0 - leftEye0
        deltaY = rightEye1 - leftEye1
        l = math.sqrt(deltaX * deltaX + deltaY * deltaY)
        sinVal = deltaY / l
        cosVal = deltaX / l
        mat1 = np.mat([[cosVal, sinVal, 0], [-sinVal, cosVal, 0], [0, 0, 1]])

        mat2 = np.mat(
            [
                [leftEye0, leftEye1, 1],
                [rightEye0, rightEye1, 1],
                [img_land[2 * 13], img_land[2 * 13 + 1], 1],
                [img_land[2 * 31], img_land[2 * 31 + 1], 1],
                [img_land[2 * 37], img_land[2 * 37 + 1], 1],
            ]
        )

        mat2 = (mat1 * mat2.T).T

        cx = float((max(mat2[:, 0]) + min(mat2[:, 0]))) * 0.5
        cy = float((max(mat2[:, 1]) + min(mat2[:, 1]))) * 0.5

        if float(max(mat2[:, 0]) - min(mat2[:, 0])) > float(
            max(mat2[:, 1]) - min(mat2[:, 1])
        ):
            halfSize = 0.5 * box_enlarge * float((max(mat2[:, 0]) - min(mat2[:, 0])))
        else:
            halfSize = 0.5 * box_enlarge * float((max(mat2[:, 1]) - min(mat2[:, 1])))

        scale = (img_size - 1) / 2.0 / halfSize
        mat3 = np.mat(
            [
                [scale, 0, scale * (halfSize - cx)],
                [0, scale, scale * (halfSize - cy)],
                [0, 0, 1],
            ]
        )
        mat = mat3 * mat1

        aligned_img = cv2.warpAffine(
            img,
            mat[0:2, :],
            (img_size, img_size),
            cv2.INTER_LINEAR,
            borderValue=(128, 128, 128),
        )

        land_3d = np.ones((int(len(img_land) / 2), 3))
        land_3d[:, 0:2] = np.reshape(np.array(img_land), (int(len(img_land) / 2), 2))
        mat_land_3d = np.mat(land_3d)
        new_land = np.array((mat * mat_land_3d.T).T)
        new_land = np.reshape(new_land[:, 0:2], len(img_land))

        return aligned_img, new_land

    def detect_au(self, imgs, land_data):
        
        land_data = np.transpose(land_data)
        if land_data.shape[-1] == 68:
           land_data = convert68to49(land_data)

        # if land_data.shape[]
        land_data = land_data.flatten()
        img, land = self.align_face_49pts(imgs, land_data)  # Transforms

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)  # Convert image to PIL

        img_transforms = transforms.Compose(
            [
                transforms.CenterCrop(176),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )

        input = img_transforms(im_pil)
        if len(input.shape) < 4:
            input.unsqueeze_(0)
        land = torch.from_numpy(land)

        if self.use_gpu:
            input, land = input.cuda(), land.cuda()

        region_feat = self.region_learning(input)
        align_feat, align_output, aus_map = self.align_net(region_feat)
        if self.use_gpu:
            aus_map = aus_map.cuda()
        output_aus_map = self.local_attention_refine(aus_map.detach())
        local_au_out_feat, local_aus_output = self.local_au_net(region_feat, output_aus_map)
        local_aus_output = (local_aus_output[:, 1, :]).exp()
        global_au_out_feat = self.global_au_feat(region_feat)
        concat_au_feat = torch.cat(
            (align_feat, global_au_out_feat, local_au_out_feat.detach()), 1
        )
        aus_output = self.au_net(concat_au_feat)
        aus_output = (aus_output[:, 1, :]).exp()
        all_output = aus_output.data.cpu().float()
        AUoccur_pred_prob = all_output.data.numpy()
        return AUoccur_pred_prob

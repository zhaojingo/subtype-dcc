import torch.nn as nn
import torch
from torch.nn.functional import normalize


class Network(nn.Module):
    def __init__(self, ae, feature_dim, class_num):
        super(Network, self).__init__()
        self.ae = ae
        self.feature_dim = feature_dim
        self.cluster_num = class_num
        
        self.instance_projector = nn.Sequential(
            nn.Linear(self.ae.rep_dim, self.ae.rep_dim),
            nn.ReLU(),
            nn.Linear(self.ae.rep_dim, self.feature_dim),
        )
        self.cluster_projector = nn.Sequential(
            nn.Linear(self.ae.rep_dim, self.ae.rep_dim),
            nn.ReLU(),
            nn.Linear(self.ae.rep_dim, self.cluster_num),
            nn.Softmax(dim=1)
        )

    def forward(self, x_i, x_j):
        h_i = self.ae(x_i)
        h_j = self.ae(x_j)

        z_i = normalize(self.instance_projector(h_i), dim=1)
        z_j = normalize(self.instance_projector(h_j), dim=1)

        c_i = self.cluster_projector(h_i)
        c_j = self.cluster_projector(h_j)

        return z_i, z_j, c_i, c_j

    def forward_cluster(self, x):
        h = self.ae(x)
        c = self.cluster_projector(h)
        c = torch.argmax(c, dim=1)
        return c,h

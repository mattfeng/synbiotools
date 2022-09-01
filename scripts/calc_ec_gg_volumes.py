import argparse
import yaml

class GoldenGateReactionCalculation():
    DNA_MOLAR_MASS_PER_BP = 650 # g/mol

    def __init__(self, backbone_bp, backbone_conc, backbone_vol):
        self.backbone_bp = backbone_bp
        self.backbone_conc = backbone_conc
        self.backbone_vol = backbone_vol
        
        backbone_molar_mass = backbone_bp * self.__class__.DNA_MOLAR_MASS_PER_BP
        backbone_mass = backbone_conc * backbone_vol
        self.backbone_moles = backbone_mass / backbone_molar_mass
    
    def calc_insert_volume(self, insert_bp, insert_conc):
        insert_molar_mass = insert_bp * self.__class__.DNA_MOLAR_MASS_PER_BP

        desired_insert_moles = 2 * self.backbone_moles
        desired_insert_mass = desired_insert_moles * insert_molar_mass

        insert_vol = desired_insert_mass / insert_conc

        return insert_vol
        

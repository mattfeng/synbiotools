import functools

from flask import Blueprint, request

bp = Blueprint("auth", __name__, url_prefix="/golden_gate")

@bp.route("", methods=["GET", "POST"])
@bp.route("/", methods=["GET", "POST"])
def golden_gate():
    if request.method == "GET":
        return "golden gate reaction calculator"

    """
    JSON data:
    {
        "backbone": {
            "name": "pL1f1",
            "bp": 4968,
            "conc": 59.1,
            "vol": 1
        },
        "inserts": [
            {
                "name": "pVEG",
                "bp": 2348,
                "conc": 108
            },
            {
                "name": "spoVG",
                "bp": 2263,
                "conc": 103.4
            },
            {
                "name": "acsAB",
                "bp": 6865,
                "conc": 119.4
            },
            {
                "name": "T001",
                "bp": 2306,
                "conc": 49
            }
        ]
    }
    """
    gg_data = request.get_json()

    results = {}

    backbone = gg_data["backbone"]
    inserts = gg_data["inserts"]

    backbone_name = backbone["name"]
    backbone_bp = backbone["bp"]
    backbone_conc = backbone["conc"]
    backbone_vol = backbone["vol"]
    calc = GoldenGateReactionCalculation(
        backbone_bp,
        backbone_conc,
        backbone_vol
        )

    for insert in inserts:
        name = insert["name"]
        bp = insert["bp"]
        conc = insert["conc"]

        vol = calc.calc_insert_volume(bp, conc)

        results[name] = {
            "vol": vol
            }
    
    return results


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
        


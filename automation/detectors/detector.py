# ---------------------------------
# COMPLETE COMPANY DETECTOR
# ---------------------------------

from automation.detectors.ats_detector import detect_ats

from automation.detectors.board_detector import detect_board

from automation.detectors.company_name_detector import detect_company_name


def detect_company(url):

    return {

        "name":

            detect_company_name(url),

        "platform":

            detect_ats(url),

        "board":

            detect_board(url)

    }
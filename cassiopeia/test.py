import sys, os
proj_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, proj_dir)

from nlp import level_assignment, nlp_training

#level_assignment.assign_levels()
#nlp_training.refresh_content_level(39)
nlp_training.refresh_user_level(39)

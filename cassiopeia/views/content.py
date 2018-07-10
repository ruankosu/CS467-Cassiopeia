import os
from flask import (
            Blueprint, flash, g, redirect, render_template, request, url_for
            )


template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, "cassiopeia")
template_dir = os.path.join(template_dir, "templates")

bp = Blueprint('content', __name__, template_folder=template_dir)

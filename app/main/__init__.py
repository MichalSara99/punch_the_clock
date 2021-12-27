from flask import Blueprint

main = Blueprint('main',__name__)

# importing view functions and error functions
# so that circular dependence is avoided
from . import views,filters,errors


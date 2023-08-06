from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.db.models import Q
from ohm2_handlers_light import utils as h_utils
from ohm2_handlers_light.definitions import RunException
from . import settings
from . import utils as matialvarezs_handlers_easy_utils
from .decorators import matialvarezs_handlers_easy_safe_request
import os, time, random


@matialvarezs_handlers_easy_safe_request
def index(request, params):
	p = h_utils.cleaned(params, (
					 	))
	
	
	ret = {
	}
	return ret
#!/bin/bash

django-admin makemessages --locale=mr_IN --locale=en_IN
django-admin compilemessages 

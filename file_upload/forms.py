# -*- coding: utf-8 -*-
"""
Copyright © 2017,
Laboratory for Atmospheric Research at Washington State University,
All rights reserved.
"""

from django import forms
from file_upload.models import Picture, Tag
from dal import autocomplete

# Choices for the tag object


def getChoices():
    T = tag.objects.values('text').distinct()

    x = []
    for g in T:
        for i, k in g.items():
            x.append((k, k))
    return x

# Theformto edit a location


class edit_location_form(forms.Form):
    geoX = forms.DecimalField(widget=forms.HiddenInput())
    geoY = forms.DecimalField(widget=forms.HiddenInput())


# The form for uploading pictures
class picture_upload_form(forms.Form):
    pic = forms.FileField(label="Select Picture")
    estimatedVr = forms.DecimalField(label="Estimated Visual Range")
    location = forms.CharField(label='Location', required=True)
    description = forms.CharField(label='Description', required=True)
    algorithmType = forms.ChoiceField(
        label='Algorithm to Apply',
        choices=[
            (1,
             "Near-Far Contrast (one image)"),
            (2,
             "Near-Far Contrast (two images)")],
        required=True)

# The form for editing algorithm one


class algorithm_one_form(forms.Form):

    # Distances to the near and far targets
    nearDistance = forms.DecimalField(
        label="Estimated distance to near target (in KM)")
    farDistance = forms.DecimalField(
        label="Estimated distance to far target (in KM)")

    # X and Y coordinates for the two circles
    nearX = forms.DecimalField(widget=forms.HiddenInput())
    nearY = forms.DecimalField(widget=forms.HiddenInput())
    farX = forms.DecimalField(widget=forms.HiddenInput())
    farY = forms.DecimalField(widget=forms.HiddenInput())

    # Radius for the circles
    farRadius = forms.DecimalField(widget=forms.HiddenInput())
    nearRadius = forms.DecimalField(widget=forms.HiddenInput())

# The form for editing algorithm two


class algorithm_two_form(forms.Form):

    # The image for the far target
    pic2 = forms.FileField(
        label="Select Picture for the far target",
        required=False)

    # Distances to the near and far targets
    nearDistance = forms.DecimalField(
        label="Estimated distance to near target (in KM)")
    farDistance = forms.DecimalField(
        label="Estimated distance to far target (in KM)")

    # Deals with circle locations
    nearX = forms.DecimalField(widget=forms.HiddenInput())
    nearY = forms.DecimalField(widget=forms.HiddenInput())
    farX = forms.DecimalField(widget=forms.HiddenInput())
    farY = forms.DecimalField(widget=forms.HiddenInput())

    # Radius of our circles
    farRadius = forms.DecimalField(widget=forms.HiddenInput())
    nearRadius = forms.DecimalField(widget=forms.HiddenInput())


def getNames():
    qs = Tag.objects.all()
    tag_names = []

    for tagy in qs:
        if (tagy.text not in tag_names):
            tag_names.append(tagy.text)
    return tag_names


# The search form for the gallery
class GallerySortForm(forms.Form):

    vr_choices = [(0, "None"), (1, '0-10'), (2, '10-30'),
                  (3, '30-100'), (4, '100-500'), (5, '500+')]
    ascending_choices = [(0, "Descending time"), (1, "Ascending time"),
                         (2, "Ascending visual Range"), (3, "Descending visual Range")]

    ascending = forms.ChoiceField(
        ascending_choices,
        label="Order by:",
        widget=forms.Select())

    visual_range = forms.ChoiceField(
        choices=vr_choices,
        label="Visual Range(in Kilometers):",
        widget=forms.Select(
            attrs={
                'id': 'vr',
                'name': 'Visual Range(in meters)',
                'class': 'form-control'}))

    # Auto complete on location
    location = autocomplete.Select2ListChoiceField(
        required=False,
        label="Location:",
        choice_list=getNames(),
        widget=autocomplete.ListSelect2(
            url='location-autocomplete'))

    date1 = forms.CharField(
        required=False,
        label="Beginning date",
        widget=forms.TextInput(
            attrs={
                'id': 'date1',
                'name': 'date-begin',
                'class': 'form-control'}))

    date2 = forms.CharField(
        required=False,
        label="End date",
        widget=forms.TextInput(
            attrs={
                'id': 'date2',
                'name': 'date-end',
                'class': 'form-control'}))

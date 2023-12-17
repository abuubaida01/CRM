# myapp/templatetags/myfilters.py

from django import template
from django.utils.timesince import timesince
from datetime import datetime
from django.utils import timezone
import re


register = template.Library()

@register.filter
def timesince_auto(value):
    now = datetime.now(timezone.utc)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    delta = now - value
    if delta.days == 0:
        minutes = int(delta.total_seconds() / 60)
        hours = int(delta.total_seconds() / 3600)
        if delta.seconds < 60:
            return "just now"
        elif delta.seconds < 120:
            return "1 min ago"
        elif delta.seconds < 3600:
            minutes = delta.seconds // 60
            return f"{minutes} mins ago"
        else:
            return f"{hours} h ago"
    elif delta.days == 1:
        return "yesterday"
    elif delta.days < 7:
        # Show time in days
        if delta.days == 1:
            return "1 d ago"
        else:
            return f"{delta.days} d ago"
    elif delta.days < 30:
        # Show time in weeks
        weeks = int(delta.days / 7)
        if weeks == 1:
            return "1 w ago"
        else:
            return f"{weeks} w ago"
    elif delta.days < 365:
        # Show time in months
        months = int(delta.days / 30)
        if months == 1:
            return "1 month"
        else:
            return f"{months} months"
    else:
        # Show time in years
        years = int(delta.days / 365)
        if years == 1:
            return "1 year"
        else:
            return f"{years}y"

@register.filter
def format_number(value):
    if value is None:
        return ""
    try:
        value = int(value)
    except (TypeError, ValueError):
        return str(value)
    if value < 1000:
        return str(value)
    elif value < 1000000:
        if value % 1000 == 0:
            return "{}K".format(int(value/1000))
        else:
            return "{:.1f}K".format(value/1000)
    elif value < 1000000000:
        if value % 1000000 == 0:
            return "{}M".format(int(value/1000000))
        else:
            return "{:.1f}M".format(value/1000000)
    elif value < 1000000000000:
        if value % 1000000000 == 0:
            return "{}B".format(int(value/1000000000))
        else:
            return "{:.1f}B".format(value/1000000000)
    else:
        if value % 1000000000000 == 0:
            return "{}T".format(int(value/1000000000000))
        else:
            return "{:.1f}T".format(value/1000000000000)

# @register.filter
# def format_rupees(value):
#     if value is None:
#         return ""
#     try:
#         value = int(value)
#     except (TypeError, ValueError):
#         return str(value)
        
#     if value < 1000:
#         return str(value)
#     elif value < 100000:
#         thousands = value // 1000
#         hundreds = (value % 1000) // 100
#         if hundreds == 0:
#             return f"{thousands} k"
#         else:
#             return f"{thousands} k, {hundreds} h"
#     elif value < 10000000:
#         lakhs = value // 100000
#         thousands = (value % 100000) // 1000
#         if thousands == 0:
#             return f"{lakhs} lakh"
#         else:
#             return f"{lakhs} lakh, {thousands} k "
#     else:
#         crores = value // 10000000
#         lakhs = (value % 10000000) // 100000
#         if lakhs == 0:
#             return f"{crores} cr"
#         else:
#             return f"{crores} crs, {lakhs} lakh "




@register.filter
def format_rupees(value):
    if value is None:
        return ""
    try:
        value = int(value)
    except (TypeError, ValueError):
        return str(value)

    if value < 1000:
        return f"{value:,}"
    elif value < 100000:
        return f"{value:,}"
    elif value < 10000000:
        return f"{value:,}"
    else:
        return f"{value:,}"

@register.filter
def truncate_string(text, length):
    if len(text) <= length:
        return text
    else:
        truncated_text = ""
        current_length = 0
        for char in text:
            truncated_text += char
            current_length += 1
            if current_length >= length:
                break
        # Remove trailing spaces
        truncated_text = truncated_text.rstrip() + "..."
        return truncated_text
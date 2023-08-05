# -*- coding: utf-8 -*-
# encoding: utf-8

import json
import re
import sys
from html.parser import HTMLParser

# from HTMLParser import HTMLParser
from odoo import models, api
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils
from odoo.addons.sm_connect.models.models_sm_wordpress_db_utils import sm_wordpress_db_utils

#TODO: Prepare cron for this task.
class sm_collaborator_fetch_wizard(models.TransientModel):
  _name = "sm_collaborators.sm_collaborator_fetch_wizard"

  @api.multi
  def create_request(self):
    self.__db_utils = sm_wordpress_db_utils.get_instance()

    # firebase fetch
    self.upcomming_members()
    return True

  def upcomming_members(self):

    # reload(sys)
    # sys.setdefaultencoding('utf8')

    feedbacks_sc = self.__db_utils.get_feedback_formcraft('Fes-te soci col·laborador')
    feedbacks_c = self.__db_utils.get_feedback_formcraft('Fes-te col·laborador')

    self.merge_feedbacks(feedbacks_sc)
    self.merge_feedbacks(feedbacks_c)

    return True

  def merge_feedbacks(self, feedbacks):

    h = HTMLParser()

    for feedback in feedbacks:

      tf = feedbacks[feedback]['content']
      df = feedbacks[feedback]['created']

      tf_utg = tf.encode('utf8')
      tf_clean = tf_utg.decode('unicode_escape')

      j = json.loads(tf_clean)

      j_comp = {}
      udata = {}
      for cs in j:
        if cs['label'] != 'Import' or (
          cs['label'] == 'Import' and cs['value'] != 'Altres' and ('Import' in j_comp) == False):
          line_key = re.sub('[^A-Za-z0-9]+', '', cs['label'])
          j_comp[line_key] = {
            'value': h.unescape(cs['value']),
            'identifier': cs['identifier']
          }

      udata['collaborator_info'] = ''
      if 'Import' in j_comp:
        udata['collaborator_info'] += str(j_comp['Import']['value'])
      if 'Periodicitat' in j_comp:
        udata['collaborator_info'] += " " + j_comp['Periodicitat']['value']

      udata['date'] = df
      udata['member_name'] = ''
      if 'Cognoms' in j_comp:
        udata['member_name'] += j_comp['Cognoms']['value']
      if 'Nom' in j_comp:
        if udata['member_name'] != '':
          udata['member_name'] += ", "
        udata['member_name'] += j_comp['Nom']['value']

      udata['name'] = df.strftime('%Y-%m-%d') + " - " + udata['member_name']
      if 'email' in j_comp:
        udata['member_email'] = j_comp['email']['value']
      udata['collaborator_type'] = 'www'

      collab = sm_utils.get_create_existing_model(self.env['sm_collaborators.sm_collaborator'],
        [('name', '=', udata['name'])], {'name': udata['name']})

      if not collab.completed:
        collab.sudo().write(udata)

    return True

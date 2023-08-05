# -*- coding: utf-8 -*-

import mysql.connector

from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils
from odoo.addons.sm_connect.models.credential_loader import credential_loader
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts


class sm_wordpress_db_utils(object):
  __instance = None

  @staticmethod
  def get_instance():
    if sm_wordpress_db_utils.__instance is None:
      sm_wordpress_db_utils()
    return sm_wordpress_db_utils.__instance

  def __init__(self):
    if sm_wordpress_db_utils.__instance is not None:
      raise Exception("This class is a singleton!")
    else:
      sm_wordpress_db_utils.__instance = self
      self._db_data = credential_loader.get_instance().get_wordpress_db_credentials()
      self.__db = False

  def get_posts(self, args=None):
    if args is None:
      args = {}

    if not self.__db:
      db_data = self._db_data['admin_data']
      self.__db = Client(str(db_data['host']).strip(),str(db_data['username']).strip(),str(db_data['password']).strip())
    return self.__db.call(posts.GetPosts(args))

  def get_post_by_id(self,post_id):
    if not self.__db:
      db_data = self._db_data['admin_data']
      self.__db = Client(db_data['host'], db_data['username'], db_data['password'])
    if int(post_id) > 0:
      return self.__db.call(posts.GetPost(post_id))
    return False

  def get_feedback_formcraft(self, form_type):
    db_data = self._db_data['db_data']
    cnx = mysql.connector.connect(user=db_data['user'], password=db_data['password'],
      host=db_data['host'],database=db_data['database'])
    cursor = cnx.cursor()
    query = "SELECT created, content FROM sm_formcraft_3_submissions WHERE form_name = '" + form_type + "'"
    cursor.execute(query)
    results = {}
    di = 0
    for (created, content) in cursor:
      results[di] = {'created': created, 'content': content}
      di = di + 1
    cursor.close()
    cnx.close()
    return results

  def get_feedback_caldera(self, form_type):
    db_data = self._db_data['db_data']
    cnx = mysql.connector.connect(user=db_data['user'], password=db_data['password'],
      host=db_data['host'],database=db_data['database'])
    cursor = cnx.cursor(buffered=True)
    meta_cursor = cnx.cursor(buffered=True)
    query = "SELECT `id` FROM `sm_cf_form_entries` WHERE `form_id` = '"+form_type+"' AND `status` = 'active'"
    cursor.execute(query)
    results = {}
    for entry_id_rs in cursor:
      entry_id = entry_id_rs[0]
      query = "SELECT slug,value FROM `sm_cf_form_entry_values` WHERE `entry_id` = "+str(entry_id)
      meta_cursor.execute(query)
      results[entry_id] = {}
      for (slug,value) in meta_cursor:
        results[entry_id].update({slug:value})
    meta_cursor.close()
    cursor.close()
    cnx.close()
    return results

  def get_post(self, coupon_id):
    if not self.__db:
      db_data = self._db_data['admin_data']
      self.__db = Client(db_data['host'], db_data['username'], db_data['password'])
    return self.__db.call(posts.GetPost(coupon_id))

  def reactivate_coupon(self, rwd):
    try:
      wp_post = self.get_post(rwd.wp_coupon_id)
    except:
      sm_utils.create_system_task(rwd,"CS company user error.","Trying to reactivate in origin coupon, but failed. rwd id: "+str(rwd.id))
      return False
    for cf in wp_post.custom_fields:
      if cf['key'] == 'coupon_used':
        cf['value'] = False
    if not self.__db:
      db_data = self._db_data['admin_data']
      self.__db = Client(db_data['host'], db_data['username'], db_data['password'])
      try:
        self.__db.call(posts.EditPost(coupon_id, wp_post))
      except:
        sm_utils.create_system_task(rwd,"CS company user error.","Trying to reactivate in origin coupon, but failed. rwd id: "+str(rwd.id))
        return False
    return  True

  # TODO: remove it's unused
  # def get_cf_entries(self,form):
  #   db_data = self._db_data['db_data']
  #   cnx = mysql.connector.connect(user=db_data['user'], password=db_data['password'],
  #     host=db_data['host'],database=db_data['database'])
  #   cursor = cnx.cursor()
  #   query = "SELECT entry_id, slug, value FROM sm_cf_form_entry_values v LEFT JOIN sm_cf_form_entries e ON e.id = v.entry_id WHERE e.form_id = '"+form+"'"
  #   cursor.execute(query)
  #   results = {}
  #   for (entry_id, slug, value) in cursor:
  #     try:
  #       results[entry_id]
  #     except:
  #       results[entry_id] = {}
  #       results[entry_id]['entry_id'] = entry_id
  #     results[entry_id][slug] = value
  #   cursor.close()
  #   cnx.close()
  #   return results
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Photos.test'
        db.add_column(u'sds_photos', 'test',
                      self.gf('django.db.models.fields.CharField')(default='yo', max_length=30),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Photos.test'
        db.delete_column(u'sds_photos', 'test')


    models = {
        u'sds.photos': {
            'Meta': {'object_name': 'Photos'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photographer': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'test': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['sds']
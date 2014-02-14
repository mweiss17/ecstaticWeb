# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Photos.url'
        db.alter_column(u'sds_photos', 'url', self.gf('django.db.models.fields.CharField')(max_length=100))

    def backwards(self, orm):

        # Changing field 'Photos.url'
        db.alter_column(u'sds_photos', 'url', self.gf('django.db.models.fields.CharField')(max_length=50))

    models = {
        u'sds.photos': {
            'Meta': {'object_name': 'Photos'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photographer': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['sds']
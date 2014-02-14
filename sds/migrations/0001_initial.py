# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Photos'
        db.create_table(u'sds_photos', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('photographer', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'sds', ['Photos'])


    def backwards(self, orm):
        # Deleting model 'Photos'
        db.delete_table(u'sds_photos')


    models = {
        u'sds.photos': {
            'Meta': {'object_name': 'Photos'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photographer': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['sds']
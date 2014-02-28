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
            ('url', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('photographer', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'sds', ['Photos'])

        # Adding model 'Events'
        db.create_table(u'sds_events', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('google_map_link', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'sds', ['Events'])

        # Adding model 'Music'
        db.create_table(u'sds_music', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('songname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('intention', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'sds', ['Music'])


    def backwards(self, orm):
        # Deleting model 'Photos'
        db.delete_table(u'sds_photos')

        # Deleting model 'Events'
        db.delete_table(u'sds_events')

        # Deleting model 'Music'
        db.delete_table(u'sds_music')


    models = {
        u'sds.events': {
            'Meta': {'object_name': 'Events'},
            'google_map_link': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sds.music': {
            'Meta': {'object_name': 'Music'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intention': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'songname': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'sds.photos': {
            'Meta': {'object_name': 'Photos'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photographer': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['sds']
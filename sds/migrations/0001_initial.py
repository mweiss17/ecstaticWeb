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
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('photoFile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('photographer', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('photoUploadDate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'sds', ['Photos'])

        # Adding model 'Music'
        db.create_table(u'sds_music', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uploadedSong', self.gf('django.db.models.fields.files.FileField')(default='uploadedSongs', max_length=100, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('songname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('song_name_or_link', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('intention', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('musicUploadDate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'sds', ['Music'])

        # Adding model 'Events'
        db.create_table(u'sds_events', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('google_map_link', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('eventPic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sds.Photos'], unique=True)),
            ('eventMix', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sds.Music'], null=True, blank=True)),
            ('fbEvent', self.gf('django.db.models.fields.URLField')(default='https://www.facebook.com/SilentDiscoSquad', max_length=200)),
            ('role1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('organizer1', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='organizerProfile1', null=True, to=orm['auth.User'])),
            ('role2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('organizer2', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='organizerProfile2', null=True, to=orm['auth.User'])),
            ('role3', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('organizer3', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='organizerProfile3', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'sds', ['Events'])

        # Adding model 'UserProfile'
        db.create_table(u'sds_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('test', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('profilePic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sds.Photos'])),
            ('signupDate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'sds', ['UserProfile'])

        # Adding model 'potentialOrganizer'
        db.create_table(u'sds_potentialorganizer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('why', self.gf('django.db.models.fields.CharField')(max_length=4095)),
        ))
        db.send_create_signal(u'sds', ['potentialOrganizer'])


    def backwards(self, orm):
        # Deleting model 'Photos'
        db.delete_table(u'sds_photos')

        # Deleting model 'Music'
        db.delete_table(u'sds_music')

        # Deleting model 'Events'
        db.delete_table(u'sds_events')

        # Deleting model 'UserProfile'
        db.delete_table(u'sds_userprofile')

        # Deleting model 'potentialOrganizer'
        db.delete_table(u'sds_potentialorganizer')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sds.events': {
            'Meta': {'object_name': 'Events'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'eventMix': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sds.Music']", 'null': 'True', 'blank': 'True'}),
            'eventPic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sds.Photos']", 'unique': 'True'}),
            'fbEvent': ('django.db.models.fields.URLField', [], {'default': "'https://www.facebook.com/SilentDiscoSquad'", 'max_length': '200'}),
            'google_map_link': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'organizer1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'organizerProfile1'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'organizer2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'organizerProfile2'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'organizer3': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'organizerProfile3'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'role1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'role2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'role3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sds.music': {
            'Meta': {'object_name': 'Music'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intention': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'musicUploadDate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'song_name_or_link': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'songname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uploadedSong': ('django.db.models.fields.files.FileField', [], {'default': "'uploadedSongs'", 'max_length': '100', 'blank': 'True'})
        },
        u'sds.photos': {
            'Meta': {'object_name': 'Photos'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photoFile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'photoUploadDate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'photographer': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'sds.potentialorganizer': {
            'Meta': {'object_name': 'potentialOrganizer'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'why': ('django.db.models.fields.CharField', [], {'max_length': '4095'})
        },
        u'sds.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profilePic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sds.Photos']"}),
            'signupDate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'test': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['sds']
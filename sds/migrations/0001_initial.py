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
            ('pictureType', self.gf('django.db.models.fields.CharField')(default='pp', max_length=2)),
            ('photoFile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('photographer', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'sds', ['Photos'])

        # Adding model 'UserProfile'
        db.create_table(u'sds_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('profilePic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sds.Photos'])),
            ('signupDate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'sds', ['UserProfile'])

        # Adding model 'Events'
        db.create_table(u'sds_events', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('google_map_link', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('eventPic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sds.Photos'], unique=True)),
            ('role1', self.gf('django.db.models.fields.CharField')(default='organizer', max_length=255)),
            ('organizer1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='organizerProfile1', null=True, to=orm['sds.UserProfile'])),
            ('role2', self.gf('django.db.models.fields.CharField')(default='organizer', max_length=255)),
            ('organizer2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='organizerProfile2', null=True, to=orm['sds.UserProfile'])),
            ('role3', self.gf('django.db.models.fields.CharField')(default='organizer', max_length=255)),
            ('organizer3', self.gf('django.db.models.fields.related.ForeignKey')(related_name='organizerProfile3', null=True, to=orm['sds.UserProfile'])),
            ('role4', self.gf('django.db.models.fields.CharField')(default='organizer', max_length=255)),
            ('organizer4', self.gf('django.db.models.fields.related.ForeignKey')(related_name='organizerProfile4', null=True, to=orm['sds.UserProfile'])),
            ('role5', self.gf('django.db.models.fields.CharField')(default='organizer', max_length=255)),
            ('organizer5', self.gf('django.db.models.fields.related.ForeignKey')(related_name='organizerProfile5', null=True, to=orm['sds.UserProfile'])),
            ('role6', self.gf('django.db.models.fields.CharField')(default='organizer', max_length=255)),
            ('organizer6', self.gf('django.db.models.fields.related.ForeignKey')(related_name='organizerProfile6', null=True, to=orm['sds.UserProfile'])),
        ))
        db.send_create_signal(u'sds', ['Events'])

        # Adding model 'Music'
        db.create_table(u'sds_music', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uploadedSong', self.gf('django.db.models.fields.files.FileField')(default='uploadedSongs', max_length=100)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('songname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('intention', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'sds', ['Music'])


    def backwards(self, orm):
        # Deleting model 'Photos'
        db.delete_table(u'sds_photos')

        # Deleting model 'UserProfile'
        db.delete_table(u'sds_userprofile')

        # Deleting model 'Events'
        db.delete_table(u'sds_events')

        # Deleting model 'Music'
        db.delete_table(u'sds_music')


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
            'eventPic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sds.Photos']", 'unique': 'True'}),
            'google_map_link': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'organizer1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organizerProfile1'", 'null': 'True', 'to': u"orm['sds.UserProfile']"}),
            'organizer2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organizerProfile2'", 'null': 'True', 'to': u"orm['sds.UserProfile']"}),
            'organizer3': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organizerProfile3'", 'null': 'True', 'to': u"orm['sds.UserProfile']"}),
            'organizer4': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organizerProfile4'", 'null': 'True', 'to': u"orm['sds.UserProfile']"}),
            'organizer5': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organizerProfile5'", 'null': 'True', 'to': u"orm['sds.UserProfile']"}),
            'organizer6': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organizerProfile6'", 'null': 'True', 'to': u"orm['sds.UserProfile']"}),
            'role1': ('django.db.models.fields.CharField', [], {'default': "'organizer'", 'max_length': '255'}),
            'role2': ('django.db.models.fields.CharField', [], {'default': "'organizer'", 'max_length': '255'}),
            'role3': ('django.db.models.fields.CharField', [], {'default': "'organizer'", 'max_length': '255'}),
            'role4': ('django.db.models.fields.CharField', [], {'default': "'organizer'", 'max_length': '255'}),
            'role5': ('django.db.models.fields.CharField', [], {'default': "'organizer'", 'max_length': '255'}),
            'role6': ('django.db.models.fields.CharField', [], {'default': "'organizer'", 'max_length': '255'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sds.music': {
            'Meta': {'object_name': 'Music'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intention': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'songname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uploadedSong': ('django.db.models.fields.files.FileField', [], {'default': "'uploadedSongs'", 'max_length': '100'})
        },
        u'sds.photos': {
            'Meta': {'object_name': 'Photos'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photoFile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'photographer': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'pictureType': ('django.db.models.fields.CharField', [], {'default': "'pp'", 'max_length': '2'})
        },
        u'sds.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profilePic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sds.Photos']"}),
            'signupDate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['sds']
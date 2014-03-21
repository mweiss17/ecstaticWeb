# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Music.songname'
        db.add_column(u'sds_music', 'songname',
                      self.gf('django.db.models.fields.CharField')(default='never gonna give you up', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Music.songname'
        db.delete_column(u'sds_music', 'songname')


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
            'eventMix': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sds.Music']"}),
            'eventPic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sds.Photos']", 'unique': 'True'}),
            'fbEvent': ('django.db.models.fields.URLField', [], {'default': "'https://www.facebook.com/SilentDiscoSquad'", 'max_length': '200'}),
            'google_map_link': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'organizer1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'organizerProfile1'", 'null': 'True', 'to': u"orm['sds.UserProfile']"}),
            'organizer2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'organizerProfile2'", 'null': 'True', 'to': u"orm['sds.UserProfile']"}),
            'organizer3': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'organizerProfile3'", 'null': 'True', 'to': u"orm['sds.UserProfile']"}),
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
            'song_name_or_link': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'songname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uploadedSong': ('django.db.models.fields.files.FileField', [], {'default': "'uploadedSongs'", 'max_length': '100', 'blank': 'True'})
        },
        u'sds.photos': {
            'Meta': {'object_name': 'Photos'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photoFile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'photographer': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'pictureType': ('django.db.models.fields.CharField', [], {'default': "'pp'", 'max_length': '2'})
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['sds']
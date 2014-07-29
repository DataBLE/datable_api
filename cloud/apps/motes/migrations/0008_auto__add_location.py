# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table(u'motes_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Default location', max_length=255)),
            ('address', self.gf('django.db.models.fields.CharField')(default='110 E 9th St', max_length=255)),
            ('city', self.gf('django.db.models.fields.CharField')(default='Los Angeles', max_length=255)),
            ('state', self.gf('django.db.models.fields.CharField')(default='CA', max_length=255)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(default='90031', max_length=255, null=True, blank=True)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')(default='POINT(0.0 0.0)', null=True, blank=True)),
        ))
        db.send_create_signal(u'motes', ['Location'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table(u'motes_location')


    models = {
        u'motes.app': {
            'Meta': {'unique_together': "(('identifier', 'platform'),)", 'object_name': 'App'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'motes.genderaction': {
            'Meta': {'object_name': 'GenderAction'},
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motes.App']"}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mote': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motes.Mote']"}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'motes.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'default': "'110 E 9th St'", 'max_length': '255'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "'Los Angeles'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Default location'", 'max_length': '255'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'default': "'POINT(0.0 0.0)'", 'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'default': "'90031'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'CA'", 'max_length': '255'})
        },
        u'motes.mote': {
            'Meta': {'unique_together': "(('uuid', 'major', 'minor'),)", 'object_name': 'Mote'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '255'}),
            'minor': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'repeat_interval': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'rssi': ('django.db.models.fields.FloatField', [], {'default': '-100'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'d882c8787078440cb528b137893f81fa'", 'max_length': '255'})
        }
    }

    complete_apps = ['motes']
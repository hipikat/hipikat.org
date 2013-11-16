# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Writing'
        db.delete_table(u'hipikat_writing')

        # Removing M2M table for field related_pages on 'Writing'
        db.delete_table(db.shorten_name(u'hipikat_writing_related_pages'))

        # Deleting model 'RichTextContent'
        db.delete_table(u'hipikat_writing_richtextcontent')

        # Deleting model 'RawContent'
        db.delete_table(u'hipikat_writing_rawcontent')

        # Deleting model 'MediaFileContent'
        db.delete_table(u'hipikat_writing_mediafilecontent')


    def backwards(self, orm):
        # Adding model 'Writing'
        db.create_table(u'hipikat_writing', (
            ('meta_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meta_keywords', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('excerpt', self.gf('django.db.models.fields.TextField')(blank=True)),
            (u'entry_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['elephantblog.Entry'], unique=True, primary_key=True)),
            ('pinging', self.gf('django.db.models.fields.SmallIntegerField')(default=10)),
        ))
        db.send_create_signal('hipikat', ['Writing'])

        # Adding M2M table for field related_pages on 'Writing'
        m2m_table_name = db.shorten_name(u'hipikat_writing_related_pages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('writing', models.ForeignKey(orm['hipikat.writing'], null=False)),
            ('page', models.ForeignKey(orm[u'page.page'], null=False))
        ))
        db.create_unique(m2m_table_name, ['writing_id', 'page_id'])

        # Adding model 'RichTextContent'
        db.create_table(u'hipikat_writing_richtextcontent', (
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='richtextcontent_set', to=orm['hipikat.Writing'])),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('text', self.gf('feincms.contrib.richtext.RichTextField')(blank=True)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('hipikat', ['RichTextContent'])

        # Adding model 'RawContent'
        db.create_table(u'hipikat_writing_rawcontent', (
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rawcontent_set', to=orm['hipikat.Writing'])),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('hipikat', ['RawContent'])

        # Adding model 'MediaFileContent'
        db.create_table(u'hipikat_writing_mediafilecontent', (
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mediafilecontent_set', to=orm['hipikat.Writing'])),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('mediafile', self.gf('feincms.module.medialibrary.fields.MediaFileForeignKey')(related_name='+', to=orm['medialibrary.MediaFile'])),
            ('type', self.gf('django.db.models.fields.CharField')(default='default', max_length=20)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('hipikat', ['MediaFileContent'])


    models = {
        
    }

    complete_apps = ['hipikat']

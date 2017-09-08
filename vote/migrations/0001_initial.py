# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-08-02 07:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('person', '0001_initial'),
        ('bill', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('congress', models.IntegerField(help_text=b'The number of the Congress in which the vote took place. The current Congress is 115. In recent history Congresses are two years; however, this was not always the case.')),
                ('session', models.CharField(help_text=b'Within each Congress there are sessions. In recent history the sessions correspond to calendar years and are named accordingly. However, in historical data the sessions may be named in completely other ways, such as with letters A, B, and C. Session names are unique *within* a Congress.', max_length=4)),
                ('chamber', models.IntegerField(choices=[(1, b'Senate'), (2, b'House')], help_text=b'The chamber in which the vote was held, House or Senate.')),
                ('number', models.IntegerField(help_text=b'The number of the vote, unique to a Congress, session, and chamber.', verbose_name=b'Vote Number')),
                ('source', models.IntegerField(choices=[(1, b'senate.gov'), (2, b'house.gov'), (3, b'VoteView.com')], help_text=b'The source of the vote information.')),
                ('created', models.DateTimeField(db_index=True, help_text=b'The date (and in recent history also time) on which the vote was held.')),
                ('vote_type', models.CharField(help_text=b'Descriptive text for the type of the vote.', max_length=255)),
                ('category', models.IntegerField(choices=[(2, b'Passage under Suspension'), (9, b'Unknown Category'), (6, b'Nomination'), (13, b'Impeachment'), (12, b'Treaty Ratification'), (3, b'Passage'), (5, b'Passage (Part)'), (7, b'Procedural'), (4, b'Cloture'), (11, b'Conviction'), (10, b'Veto Override'), (1, b'Amendment')], help_text=b'The type of the vote.')),
                ('question', models.TextField(help_text=b'Descriptive text for what the vote was about.')),
                ('required', models.CharField(help_text=b"A code indicating what number of votes was required for success. Often '1/2' or '3/5'. This field should be interpreted with care. It comes directly from the upstream source and may need some 'unpacking.' For instance, while 1/2 always mean 1/2 of those voting (i.e. excluding absent and abstain), 3/5 in some cases means to include absent/abstain and in other cases to exclude.", max_length=10)),
                ('result', models.TextField(help_text=b'Descriptive text for the result of the vote.')),
                ('total_plus', models.IntegerField(blank=True, default=0, help_text=b'The count of positive votes (aye/yea).')),
                ('total_minus', models.IntegerField(blank=True, default=0, help_text=b'The count of negative votes (nay/no).')),
                ('total_other', models.IntegerField(blank=True, default=0, help_text=b'The count of abstain or absent voters.')),
                ('percent_plus', models.FloatField(blank=True, help_text=b"The percent of positive votes. Null for votes that aren't yes/no (like election of the speaker, quorum calls).", null=True)),
                ('margin', models.FloatField(blank=True, help_text=b"The absolute value of the difference in the percent of positive votes and negative votes. Null for votes that aren't yes/no (like election of the speaker, quorum calls).", null=True)),
                ('missing_data', models.BooleanField(default=False, help_text=b'If something in the source could be parsed and we should revisit the file.')),
                ('question_details', models.TextField(blank=True, help_text=b'Additional descriptive text for what the vote was about.', null=True)),
                ('related_amendment', models.ForeignKey(blank=True, help_text=b'A related amendment.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='votes', to='bill.Amendment')),
                ('related_bill', models.ForeignKey(blank=True, help_text=b'A related bill.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='votes', to='bill.Bill')),
            ],
            options={
                'ordering': ['created', 'chamber', 'number'],
            },
        ),
        migrations.CreateModel(
            name='VoteOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=20)),
                ('value', models.CharField(max_length=255)),
                ('vote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='vote.Vote')),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voter_type', models.IntegerField(choices=[(2, b'Vice President'), (1, b'Unknown'), (3, b'Member of Congress')], help_text=b'Whether the voter was a Member of Congress or the Vice President.')),
                ('voteview_extra_code', models.CharField(help_text=b'Extra information provided in the voteview data.', max_length=20)),
                ('created', models.DateTimeField(db_index=True, help_text=b'The date (and in recent history also time) on which the vote was held.')),
                ('option', models.ForeignKey(help_text=b'How the person voted.', on_delete=django.db.models.deletion.CASCADE, to='vote.VoteOption')),
                ('person', models.ForeignKey(blank=True, help_text=b'The person who cast this vote. May be null if the information could not be determined.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='votes', to='person.Person')),
                ('person_role', models.ForeignKey(blank=True, help_text=b'The role of the person who cast this vote at the time of the vote. May be null if the information could not be determined.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='votes', to='person.PersonRole')),
                ('vote', models.ForeignKey(help_text=b'The vote that this record is a part of.', on_delete=django.db.models.deletion.CASCADE, related_name='voters', to='vote.Vote')),
            ],
        ),
        migrations.CreateModel(
            name='VoteSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(blank=True)),
                ('vote', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='oursummary', to='vote.Vote')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('congress', 'chamber', 'session', 'number')]),
        ),
    ]
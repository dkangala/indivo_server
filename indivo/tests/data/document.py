from indivo.models import Document
from base import *
import hashlib

class TestDocument(TestModel):
    model_fields = ['content', 'record', 'pha', 'label', 'creator', 'external_id', 'mime_type']
    model_class = Document

    def _setupargs(self, content, record=None, pha_spec=False, 
                 pha=None, label='testing', creator=None, external_id=None, mime_type='application/xml'):
        self.content = content
        self.mime_type = mime_type
        self.record = record
        self.pha = pha
        self.local_external_id = external_id
        if self.pha:
            self.external_id = Document.prepare_external_id(external_id, self.pha, pha_spec, record)
        else:
            self.external_id = None

        if not pha_spec:
            self.pha = None

        self.label = label
        self.creator = creator

    def save(self):
        """ Special case: original_id might be a pointer to self, which ForeignKey doesn't support. """
        super(TestDocument, self).save()
        if not Document.objects.filter(pk=self.django_obj.original_id).exists():
            self.django_obj.original = None
            self.django_obj.save()

        return self.django_obj

# TEST_DOCS have no default records: they should always be created with override args of
# (at least) record=some_existing_record

# Docs 1-5 have external ids, docs 6-11 don't
_TEST_R_DOCS = [
    {'label':'rdoc1',
     'content':"<Document id='HELLOWORLD00' xmlns='http://indivo.org/vocab#'></Document>",
     'record': None,
     'pha': ForeignKey('app', 'TEST_USERAPPS',0),
     'creator': ForeignKey('app', 'TEST_USERAPPS', 0),
     'external_id':'external_rdoc1',
     'pha_spec':False
     },
    {'label':'rdoc2',
     'content':"<Document id='HELLOWORLD01' xmlns='http://indivo.org/vocab#'></Document>",
     'record': None,
     'pha': ForeignKey('app', 'TEST_USERAPPS',0),
     'creator': ForeignKey('app', 'TEST_USERAPPS', 0),
     'external_id':'external_rdoc2',
     'pha_spec':False
     },
    {'label':'rdoc3',
     'content':"<Document id='HELLOWORLD02' xmlns='http://indivo.org/vocab#'></Document>",
     'record': None,
     'pha': ForeignKey('app', 'TEST_USERAPPS',0),
     'creator': ForeignKey('app', 'TEST_USERAPPS', 0),
     'external_id':'external_rdoc3',
     'pha_spec':False
     },    
    {'label':'rdoc4',
     'content':"<Document id='HELLOWORLD03' xmlns='http://indivo.org/vocab#'></Document>",
     'record': None,
     'pha': ForeignKey('app', 'TEST_USERAPPS',0),
     'creator': ForeignKey('app', 'TEST_USERAPPS', 0),
     'external_id':'external_rdoc4',
     'pha_spec':False
     },
    {'label':'rdoc5',
     'content':"<Document id='HELLOWORLD04' xmlns='http://indivo.org/vocab#'></Document>",
     'record': None,
     'pha': ForeignKey('app', 'TEST_USERAPPS',0),
     'creator': ForeignKey('app', 'TEST_USERAPPS', 0),
     'external_id':'external_rdoc5',
     'pha_spec':False
     },
    {'label':'rdoc6',
     'content':"<Document id='HELLOWORLD05' xmlns='http://indivo.org/vocab#'></Document>",
     'record': None, 
     'creator': ForeignKey('app', 'TEST_USERAPPS', 0),
      },
    {'label':'rdoc7',
     'content':"<Document id='HELLOWORLD06' xmlns='http://indivo.org/vocab#'></Document>",
     'record': None,
     'creator': ForeignKey('app', 'TEST_USERAPPS', 0),
 
     },
    {'label':'rdoc8',
     'content':"<Document id='HELLOWORLD07' xmlns='http://indivo.org/vocab#'></Document>",
     'record': None,
     'creator': ForeignKey('app', 'TEST_USERAPPS', 0),
     },
    {'label':'rdoc9',
     'content':"<Document id='HELLOWORLD08' xmlns='http://indivo.org/vocab#'></Document>",
     'record': None,
     'creator': ForeignKey('app', 'TEST_USERAPPS', 0),
     },
    {'label':'rdoc10',
     'content':"<Document id='HELLOWORLD09' xmlns='http://indivo.org/vocab#'></Document>",
     'record': None, 
     'creator': ForeignKey('app', 'TEST_USERAPPS', 0),
     },
    {'label':'rdoc11', # The crazy one
     'content':"<CrazyDocument id='HELLOWORLD10' xmlns='http://indivo.org/vocab#'></CrazyDocument>",
     'record': None, 
     'creator': ForeignKey('app', 'TEST_USERAPPS', 0),
     },
]
TEST_R_DOCS = scope(_TEST_R_DOCS, TestDocument)

# Doc 1 has no ext_id, Doc 2 does
_TEST_RA_DOCS = [
    {'label':'radoc1',
     'content':"<Document id='HELLOWORLD01' xmlns='http://indivo.org/vocab#'></Document>",
     'record': None, 
     'pha': ForeignKey('app', 'TEST_USERAPPS',0),
     'creator': ForeignKey('app', 'TEST_USERAPPS', 0),
     'pha_spec':True
     },
    {'label':'radoc2',
     'content':"<Document id='HELLOWORLD02' xmlns='http://indivo.org/vocab#'></Document>",
     'record': None, 
     'pha': ForeignKey('app', 'TEST_USERAPPS',0),
     'creator': ForeignKey('app', 'TEST_USERAPPS', 0),
     'external_id':'external_radoc2',
     'pha_spec':True
     },
]
TEST_RA_DOCS = scope(_TEST_RA_DOCS, TestDocument)

# Doc 1 has no ext_id, Doc 2 does
_TEST_A_DOCS = [
    {'label':'adoc1',
     'content':"<Document id='HELLOWORLD01' xmlns='http://indivo.org/vocab#'></Document>",
     'pha': ForeignKey('app', 'TEST_USERAPPS',0),
     'creator': ForeignKey('app', 'TEST_USERAPPS', 0),
     'pha_spec':True
     },
    {'label':'adoc2',
     'content':"<Document id='HELLOWORLD02' xmlns='http://indivo.org/vocab#'></Document>",
     'pha': ForeignKey('app', 'TEST_USERAPPS',0),
     'creator': ForeignKey('app', 'TEST_USERAPPS', 0),
     'external_id':'external_adoc2',
     'pha_spec':True
     },
]
TEST_A_DOCS = scope(_TEST_A_DOCS, TestDocument)

_TEST_DEMOGRAPHICS_DOCS = [
    {'label':'demo1',
     'record':None,
     'content':'''<Demographics xmlns="http://indivo.org/vocab/xml/documents#">
                    <dateOfBirth>1939-11-15</dateOfBirth>
                    <gender>male</gender>
                    <email>test@fake.org</email>
                    <ethnicity>Scottish</ethnicity>
                    <preferredLanguage>EN</preferredLanguage>
                    <race>caucasian</race>
                    <Name>
                        <familyName>Wayne</familyName>
                        <givenName>Bruce</givenName>
                        <prefix>Mr</prefix>
                        <suffix>Jr</suffix>
                    </Name>
                    <Telephone>
                        <type>h</type>
                        <number>555-5555</number>
                        <preferred>true</preferred>
                    </Telephone>
                    <Telephone>
                        <type>c</type>
                        <number>555-6666</number>
                        <preferred>false</preferred>
                    </Telephone>
                    <Address>
                        <country>USA</country>
                        <city>Gotham</city>
                        <postalCode>90210</postalCode>
                        <region>secret</region>
                        <street>1007 Mountain Drive</street>
                    </Address>
                </Demographics>'''},  
    {'label':'demo1',
     'record':None,
     'content':'''<Demographics xmlns="http://indivo.org/vocab/xml/documents#">
                    <dateOfBirth>1975-01-19</dateOfBirth>
                    <gender>female</gender>
                    <email>test2@fake.org</email>
                    <ethnicity>Scottish</ethnicity>
                    <preferredLanguage>english</preferredLanguage>
                    <race>caucasian</race>
                    <Name>
                        <familyName>Testerson</familyName>
                        <givenName>Test</givenName>
                    </Name>
                    <Telephone>
                        <type>h</type>
                        <number>555-5555</number>
                        <preferred>true</preferred>
                    </Telephone>
                    <Telephone>
                        <type>c</type>
                        <number>555-6666</number>
                    </Telephone>
                    <Address>
                        <country>USA</country>
                        <city>Gotham</city>
                        <postalCode>90210</postalCode>
                        <region>secret</region>
                        <street>1007 Mountain Drive</street>
                    </Address>
                </Demographics>'''},
    {'label':'demo1',
     'record':None,
     'content':'''<Demographics xmlns="http://indivo.org/vocab/xml/documents#">
                    <dateOfBirth>1985-06-01</dateOfBirth>
                    <gender>female</gender>
                    <email>test3@fake.org</email>
                    <ethnicity>Scottish</ethnicity>
                    <preferredLanguage>english</preferredLanguage>
                    <race>caucasian</race>
                    <Name>
                        <familyName>McGee</familyName>
                        <givenName>Testy</givenName>
                    </Name>
                    <Telephone>
                        <type>h</type>
                        <number>555-5555</number>
                        <preferred>true</preferred>
                    </Telephone>
                    <Telephone>
                        <type>c</type>
                        <number>555-6666</number>
                    </Telephone>
                    <Address>
                        <country>USA</country>
                        <city>Gotham</city>
                        <postalCode>90210</postalCode>
                        <region>secret</region>
                        <street>1007 Mountain Drive</street>
                    </Address>
                </Demographics>'''},
]
TEST_DEMOGRAPHICS_DOCS = scope(_TEST_DEMOGRAPHICS_DOCS, TestDocument)


#! /usr/bin/python2.3
# vim:sw=8:ts=8:et:nowrap
import sys
import re
import os
import string


# In Debian package python2.3-egenix-mxdatetime
import mx.DateTime


from miscfuncs import ApplyFixSubstitutions

from splitheadingsspeakers import SplitHeadingsSpeakers
from splitheadingsspeakers import StampUrl

from clsinglespeech import qspeech
from parlphrases import parlPhrases

from miscfuncs import FixHTMLEntities
from miscfuncs import WriteXMLFile

from filterwransques import FilterQuestion
from filterwransreply import FilterReply

from contextexception import ContextException

fixsubs = 	[
	('<intro><date> </intro><dpthd>', '', 1, '2003-10-06'), 
	('how many crimes have been', '\\1 (1)', 1, '2004-03-04'),
        ( '<xref locref=390>', '', 1, '2003-06-19'),
        ( '</FONT></FONT></TD></TR>', '', 1, '2003-07-11'),
        ( 'It is a matter for the ', '(3) It is a matter for the ', 1, '2003-07-16'),
	( '<h2><center>written answers to</center></h2>\s*questions(?i)', \
	  	'<h2><center>Written Answers to Questions</center></h2>', -1, 'all'),
	( '<h\d align=center>written answers[\s\S]{10,150}?\[continued from column \d+?W\](?:</h\d>)?(?i)', '', -1, 'all'),
	( '<h\d><center>written answers[\s\S]{10,150}?\[continued from column \d+?W\](?i)', '', -1, 'all'),
 

	( '<H2 align=center> </H2>', '', 1, '2003-09-15'),
	( '<H1 align=center></H1>\s*<H2 align=center>Monday 15 September 2003</H2>', '', 1, '2003-09-15'),
	( '<H1 align=center></H1>', '', 1, '2003-10-06'),


        ( '(\<UL\>\(2\) what research work he has \<i\>\(a\)</i> commissioned and \<i\>\(b\)\</i\> evaluated on external)(\<P\>\</UL\>)', '\\1 counter pulsation; and what conclusions about its efficacy were drawn. [143813] \\2', 1, '2003-12-16'),


	# sort out a lot of nasty to-ask problems
	( 'To as the Deputy Prime Minister', 'To ask the Deputy Prime Minister', 1, '2003-10-06'),
	( '\n What ', '\n To ask the Secretary of State for Northern Ireland what ', 4, '2003-09-10'),
	( '\n If he will ', '\n To ask the Secretary of State for Northern Ireland if he will ', 2, '2003-09-10'),

 	( '\n If he will ', '\n To ask the Secretary of State for Scotland if he will ', 1, '2003-09-09'),
 	( '\n How many ', '\n To ask the Secretary of State for Scotland how many ', 1, '2003-09-09'),
 	( '\n What recent ', '\n To ask the Secretary of State for Scotland what recent ', 2, '2003-09-09'),
 	( '\n When he ', '\n To ask the Secretary of State for Scotland when he ', 2, '2003-09-09'),

 	( '\n If he ', '\n To ask the Secretary of State for Work and Pensions if he ', 2, '2003-07-07'),
 	( '\n What ', '\n To ask the Secretary of State for Work and Pensions what ', 2, '2003-07-07'),
 	( '\n How many ', '\n To ask the Secretary of State for Work and Pensions how many ', 1, '2003-07-07'),
 	( '\n What ', '\n To ask the Secretary of State for Culture, Media and Sport what ', 1, '2003-06-30'),

 	( ' What assessment', '\n To ask the Secretary of State for Culture, Media and Sport what ', 1, '2004-03-08'),

 	( ' (on military flights at Northolt)', 'To ask the Secretary of State for Defence SOMETHING \\1', 1, '2003-06-03'),
	( '\n When he expects', '\nTo ask the Secretary of State for Education and Skills when he expects', 1, '2003-04-10'),
	( '\n Asked the Secretary', '\nTo ask the Secretary', 1, '2003-03-21'),
	( ' What (measures will be)', 'To ask the Secretary of State for Work and Pensions what \\1', 1, '2003-03-17'),

	( ' What (plans he has to reform)', 'To ask the Chancellor of the Exchequer what \\1', 1, '2004-01-29'),
	( ' If (he will make a statement)', 'To ask the Chancellor of the Exchequer if \\1', 2, '2004-01-29'),
	( '( To) (the Secretary of State for Trade and Industry)', '\\1 ask \\2', 1, '2004-01-26'),


	( '\((115021)\)', '[\\1]', 1, '2003-06-03'),
	( '\{\*\*con\*\*\}\{\*\*/con\*\*\}', '', 1, '2003-05-19'),
        ( '(\[142901)', '\\1]', 1, '2003-12-11'),

        ( '(&nbsp;a minimum energy)<P>', '\\1 efficiency rating.  [153278]', 1, '2004-02-10'),
        ( '(what the countries of origin were; and if he will make a statement.)', '\\1 [147100]', 1, '2004-01-15'),
        
 	( '\n To as the Secretary', '\n To ask the Secretary', 2, '2003-01-14'),
 	( '\n To\s*ask ', '\n To ask ', 7, '2003-04-10'),
 	( '\n To\s*ask ', '\n To ask ', 9, '2003-03-06'),
 	( '\n To\s*ask ', '\n To ask ', 37, '2003-01-27'),

        ( 'To (the Secretary of State for Environment)', 'To ask \\1', 1, '2004-02-25'),
        ( '(Rural Affairs) (what discussions)', '\\1 (1) \\2', 1, '2004-02-25'),
        ( '<P align=left>\[Continued from column 536W\]</P>', '', 1, '2004-02-26'),

	( '(column 45W\.)\[(108495)\]', '\\1 reference \\2', 1, '2003-04-28'),
        ( '(To ask the Secretary of State for Health) (for how many former community)', '\\1 (1) \\2', 1, '2004-02-23'),

 	( 'Worcestershire</FONT></TD>', 'Worcestershire', 1, '2003-07-15'),

	( '\{\*\*con\*\*\}\{\*\*/con\*\*\}', '', 3, '2002-07-24'),
	( '\{\*\*con\*\*\}\{\*\*/con\*\*\}', '', 1, '2003-01-13'),
	( '\n\s*\(1\)\s*To ask', '\n To ask (1) ', 3, '2002-07-24'),

	( 'how the proposed', '(1) how the proposed', 1, '2003-04-28'),
	( 'Cabinet Office if', 'Cabinet Office (1) if', 1, '2003-04-03'),
	( '<P>\s*<UL> (\[106584\])<P></UL>', '\\1', 1, '2003-04-01'),
	( 'Home Department when he will', 'Home Department (1) when he will', 1, '2003-03-13'),
 	( '\(1\) Asked (the Secretary of State for International Development) what', ' To ask \\1 (1) what', 1, '2003-03-07'),
 	( ' Asked the Secretary', 'To ask the Secretary', 7, '2003-03-07'),
	( 'Commonwealth Affairs what assessment', 'Commonwealth Affairs (1) what assessment', 1, '2003-03-07'),
 	( '\n What discussions he', '\nTo ask the Secretary of State for Wales what discussions he', 2, '2003-02-12'),
	( '\{\*\*con\*\*\}\{\*\*/con\*\*\}', '', 1, '2003-01-30'),
	( 'Rural Affairs what estimates', 'Rural Affairs (1) what estimates', 1, '2003-01-29'),
        

	( '(<UL>) (<i>\(a\)</i>&nbsp;housing associations)', '\\1 (2) \\2', 1, '2004-03-05' ),

	( 'Vol. No. 412,', '', 1, '2003-11-10'),
	( '</TH></TH>', '</TH>', 1, '2003-11-17'),

	( '2003&#150;11&#150;21', '2003', 1, '2003-11-20'),
	( '27Ooctober', '27 October', 1, '2003-10-27'),

	( '<TABLE BORDER=1>\s*<P>\s*</FONT></TH></TR>', '<TABLE BORDER=1>', 2, '2002-10-22'),



	( '131278\]', ' [131278]', 1, '2003-10-06'),
	( 'Department how many asylum applications', 'Department (1) how many asylum applications', 1, '2003-09-18'),

	#( '<TABLE BORDER=1>\s*<H4>', '<H4>', 6, '2002-10-22'),

	( '"</i>Guidance', '</i>"Guidance', 1, '2003-10-30'),


	# broken link fixing material
	( 'standards.php\*', 'standards.php', 1, '2003-12-08'),
	( 'http://www/', 'http://www.', 1, '2003-11-03'),
	( 'www.mod.ukyissues', 'www.mod.uk/issues', 1, '2003-10-22'),
	( 'http.V/', 'http://', 1, '2003-09-18'),
	( 'hhtp://', 'http://', 1, '2003-09-08'),
	( 'http:www', 'http://www', 1, '2003-07-17'),
	( 'www.lshtm.ac/', 'www.lshtm.ac.uk/', 1, '2003-07-10'),
	( 'www.g8.fr.Evian', 'www.g8.fr/evian', 1, '2003-06-13'),
	( 'http//wwwstatisticsgovuk/', 'http//www.statistics.gov.uk/', 1, '2003-09-01'),
	( 'http:www', 'http://www', 1, '2003-07-01'),
	( 'www.mod.ulc', 'www.mod.uk', 1, '2003-01-15'),
	( 'www://defraweb', 'http://defraweb', 1, '2003-05-07'),
	( 'www.hypo-org', 'www.hypo.org', 1, '2003-04-29'),
	( 'www.btselem.orR', 'www.btselem.org', 1, '2003-04-14'),
	( 'www.unicef-org', 'www.unicef.org', 1, '2003-02-28'),
	( 'gov.ukyStatBase', 'gov.uk/StatBase', 1, '2003-05-22'),
        ( 'defraweb', 'www.defra.gov.uk', 1, '2003-12-18'),
        ( 'sn99&#150;35\(s.htm\);', 'sn99-35s.htm;', 1, '2003-07-16'),

        # special note not end of block - when we have multiple answers
        ( '(Decisions on proposed closures of post offices are an operational matter for Post Office Ltd)', '<another-answer-to-follow>\\1', 1, '2004-01-22'),
        ( '(This includes securing the treatment, storage, transportation and disposal of radioactive waste)', '<another-answer-to-follow>\\1', 1, '2004-03-15'),
]






# parse through the usual intro headings at the beginning of the file.
def StripWransHeadings(headspeak, sdate):
	# check and strip the first two headings in as much as they are there
	i = 0
	if (headspeak[i][0] != 'Initial') or headspeak[i][2]:
		print headspeak[0]
		raise Exception, 'non-conforming Initial heading '
	i += 1

	if (not re.match('written answers to questions(?i)', headspeak[i][0])) or headspeak[i][2]:
		if not re.match('The following answers were received.*', headspeak[i][0]):
			print headspeak[i]
			raise Exception, 'non-conforming Initial heading '
	else:
		i += 1

	if (not re.match('The following answers were received.*', headspeak[i][0]) and
            not re.match('The following question was answered on.*', headspeak[i][0]) and \
			(sdate != mx.DateTime.DateTimeFrom(string.replace(headspeak[i][0], "&nbsp;", " ")).date)) or headspeak[i][2]:
		if (not parlPhrases.wransmajorheadings.has_key(headspeak[i][0])) or headspeak[i][2]:
			print headspeak[i]
			raise Exception, 'non-conforming second heading '
	else:
		i += 1

	# find the url and colnum stamps that occur before anything else
	stampurl = StampUrl(sdate)
	for j in range(0, i):
		stampurl.UpdateStampUrl(headspeak[j][1])

	if (not stampurl.stamp) or (not stampurl.pageurl) or (not stampurl.aname):
		raise Exception, ' missing stamp url at beginning of file '
	return (i, stampurl)







################
# main function
################
def FilterWransSections(fout, text, sdate):
	text = ApplyFixSubstitutions(text, sdate, fixsubs)
	headspeak = SplitHeadingsSpeakers(text)

	# break down into lists of headings and lists of speeches
	(ih, stampurl) = StripWransHeadings(headspeak, sdate)


	# full list of question batches
	# We create a list of lists of speeches
	flatb = [ ]
	for sht in headspeak[ih:]:
		# triplet of ( heading, unspokentext, [(speaker, text)] )
		headingtxt = string.strip(sht[0])
		unspoketxt = sht[1]
		speechestxt = sht[2]

                # Cases where a heading spreads out of its centre tag into
                # the next bit.  Happens a lot in wrans in January 2003.
                # e.g. In 2003-01-15 we have heading "Birmingham Northern Relief Road "
                # with extra bit "(Low-noise Tarmac)" to pull in.
                bhmatch = re.match('(\s*[()A-Za-z\-\' ]+)([\s\S]*)$', unspoketxt)
                if bhmatch:
                        # Merge the heading part back in
                        headingtxt = headingtxt + bhmatch.group(1)
                        headingtxt = re.sub("\s+", " ", headingtxt)
                        unspoketxt = bhmatch.group(2)
                        print "Merged into heading: ", headingtxt
                  

		# update the stamps from the pre-spoken text
		if (not re.match('(?:<[^>]*>|\s)*$', unspoketxt)):
			print sht
			raise Exception, "unspoken text under heading in wrans"
		stampurl.UpdateStampUrl(unspoketxt)

		# headings become one unmarked paragraph of text

		# detect if this is a major heading
		if not re.search('[a-z]', headingtxt) and not speechestxt:
			if not parlPhrases.wransmajorheadings.has_key(headingtxt):
				print '"%s":"%s",' % (headingtxt, headingtxt)
				raise Exception, "unrecognized major heading, please add to parlPhrases.wransmajorheadings"
			majheadingtxtfx = parlPhrases.wransmajorheadings[headingtxt] # no need to fix since text is from a map.
			qbH = qspeech('nospeaker="true"', majheadingtxtfx, stampurl)
			qbH.typ = 'major-heading'
			qbH.stext = [ majheadingtxtfx ]
			flatb.append(qbH)
			continue


		# non-major heading; to a question batch
		if parlPhrases.wransmajorheadings.has_key(headingtxt):
			raise Exception, ' speeches found in major heading %s' % headingtxt

		headingtxtfx = FixHTMLEntities(headingtxt)
		headingmark = 'nospeaker="True"'
		bNextStartofQ = True

		# go through each of the speeches in a block and put it into our batch of speeches
		qnums = []	# used to account for spurious qnums seen in answers
		for ss in speechestxt:
			qb = qspeech(ss[0], ss[1], stampurl)
			#print ss[0] + "  " + stampurl.stamp
			lqnums = re.findall('\[(\d+)R?\]', ss[1])

			# question posed
			if re.match('(?:<[^>]*?>|\s)*?(to ask)(?i)', qb.text):
				qb.typ = 'ques'

				# put out the heading for this question-reply block.
				# we don't assert true since we can have multiple questions answsered in a block.
				if bNextStartofQ:
					# put out a heading
					# we need to make the heading of from the same stampurl as the first question
					qbh = qspeech(headingmark, headingtxtfx, qb.sstampurl)
					qbh.typ = 'minor-heading'
					qbh.stext = [ headingtxtfx ]
					flatb.append(qbh)

					bNextStartofQ = False

					# used to show that the subsequent headings in this block have been created,
					# and weren't in the original text.
					headingmark = 'nospeaker="True" inserted-heading="True"'
					qnums = lqnums # reset the qnums count
				else:
					qnums.extend(lqnums)

				qb.stext = FilterQuestion(qb.text, sdate)
				if not lqnums:
					errmess = ' <p class="error">Question number missing in Hansard, possibly truncated question.</p> '
					qb.stext.append(errmess)

				flatb.append(qb)

			# do the reply
			else:
				if bNextStartofQ:
					raise Exception, ' start of question expected '
				qb.typ = 'reply'

				# this case is so rare we flag them in the corrections of the html with this tag
				if re.search("\<another-answer-to-follow\>", qb.text):
					qb.text = qb.text.replace("<another-answer-to-follow>", "")
				else:
					bNextStartofQ = True

				qb.stext = FilterReply(qb.text)

				# check against qnums which are sometimes repeated in the answer code
				for qn in lqnums:
					# sometimes [n] is an enumeration or part of a title
					nqn = string.atoi(qn)
					if (not qnums.count(qn)) and (nqn > 100) and ((nqn < 1995) or (nqn > 2003)):
						print ' unknown qnum present in answer ' + qb.sstampurl.stamp
						print qn
						raise Exception, ' make it clear '
						self.stext.append('<p class="error">qnum present in answer</p>')

				flatb.append(qb)

		if not bNextStartofQ:
                        # Note - not sure if this should be speechestxt[0][1] here.  Does what I want for now...
			raise ContextException("missing answer to question", stamp=stampurl, fragment=speechestxt[0][1])


	# we now have everything flattened out in a series of speeches,
	# where some of the speeches are headings (inserted and otherwise).

	# output the list of entities
	WriteXMLFile(fout, flatb, sdate)

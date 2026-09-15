# TC-012/017/019/020/021 Annex A 默认消息内容（官方 .3.3 等价）

来源：`3GPP TS 34.229-1` V14.7.0 (2019-06) Annex A，逐行抽取自 `C:\Users\co1750\Documents\Codex\2026-09-02\i\_extract\34229-1e70-word.txt`；行号口径 `Python str.splitlines()`。

说明：MO/MT 呼叫、保持/恢复、会议相关用例的 Expected sequence 均引用 Annex A 默认消息（如 `Use the default message "INVITE" in annex A.2.1 ...`），因此这些表就是对应用例的 `.3.3 Specific message contents` 等价物。

## A.2.1 INVITE for MO Call Setup（行 23435-24112；used_by: TC-012, TC-020, TC-021）

关键官方标记：`INVITE`、`Request-URI`、`100rel`、`Supported`、`P-Early-Media`、`Content-Type`

```text
23435: A.2.1	INVITE for MO Call Setup
23436: Header/param
23437: Cond
23438: Value/remark
23439: Rel
23440: Reference
23441: Request-Line
23446: 	Method
23448: INVITE
23450: RFC 3261 [15]
23451: 	Request-URI
23452: NOT A5
23453: px_IMS_CalleeUri
23454: px_IMS_CalleeURI may be either SIP or Tel URI. It may contain a dialstring and phone-context parameter, when calling to dialstring. When calling to dialstring SIP URI must also contain user=phone or user=dialstring parameter.
23455: The dialstring, if used, may be global, home local number or geo-local number. For home local numbers the value of phone-context parameter must equal the home domain name i.e. px_IMS_HomeDomainName. For geo-local numbers the home domain name must be prefixed by string "geo-local." or access technology specific prefix, if the UE supports that option.
23456: Note: The way how the UE determines whether numbers in a non-international format are geo-local, home-local or relating to another network, is UE implementation specific. For instance the UE might have a UI setting
23458: TS 24.229 [10]
23459: cl 5.1.2A.1.3, 5.1.2A.1.5, 7.2A.10
23461: A5
23462: px_IMS_CalleeContactUri
23466: A6,A7
23467: emergency service URN beginning with urn:service:sos
23469: RFC 5031 [97]
23471: A20 AND (NOT A25)
23472: urn:service:sos.ecall.manual
23474: Rel-14
23475: RFC 8147 [149]
23477: A21 AND (NOT A25)
23478: urn:service:sos:ecall.automatic
23479: Rel-14
23480: RFC 8147 [149]
23482: A25
23483: The Test URI as per the generic "eCall test URI" which uses EFSDNURI from table 4.9.3.5-1 for "eCall capable" UEs or EFFDNURI from table 4.9.3.5-2 for "eCall only" UEs as specified in 3GPP TS 36.508 [94]
23484: Rel-14
23485: RFC 8147 [149]
23486: 	SIP-Version
23488: SIP/2.0
23491: Via
23495: RFC 3261 [15]
23496: 	sent-protocol
23498: SIP/2.0/UDP (when using UDP) or
23499: SIP/2.0/TCP (when using TCP)
23502: 	sent-by
23503: A1,A7
23504: IP address or FQDN and protected server port of the UE
23508: A2,A19
23509: IP address or FQDN, port (optional) and not checked
23513: A6
23514: IP address and, when using UDP, unprotected server port of the UE
23518: A17
23519: IP address and unprotected server port of the UE
23522: 	response-port
23523: A6
23524: rport (when using UDP)
23526: RFC 3581 [96]
23527: 	via-branch
23529: value starting with 'z9hG4bK'
23532: Route
23534: order of the parameters in this header must be like in the respective rows
23536: RFC 3261 [15]
23537: 	route-param
23538: A1
23539: <sip:SS P-CSCF address: protected server port of SS;lr>, <sip:scscf.3gpp.org;lr>
23543: A2,A17
23544: <sip:SS P-CSCF address: unprotected server port of SS (optional);lr>, <sip:scscf.3gpp.orgf;lr
23548: A5
23549: MO call has been established:
23550: URIs of the Record-Route header of 183 response in reverse order (or any other response creating the dialog according to RFC 3261 clause 12.1 [15])
23552: MT call has been established:
23553: same value as defined for the Record-Route header in A.2.9
23557: A6,A19
23558: <sip:SS P-CSCF address: unprotected server port of SS;lr>
23562: A7
23563: <sip:SS P-CSCF address: protected server port of SS;lr>
23566: From
23570: RFC 3261 [15]
23571: 	addr-spec
23572: A6
23573: Any SIP URI with display name as "Anonymous" or anonymous
23577: A7,A19
23578: emergency public user identity (NOTE 3)
23582: A4
23583: any SIP URI being subscribed and registered as listed in the XML body of the NOTIFY request; additionally when there is a P-Preferred-Identity header within the INVITE request the SIP URI shall match the URI within the P-Preferred-Identity header
23586: 	tag
23587: A4
23588: must be present, value not checked
23591: 	addr-spec
23592: A5
23593: local SIP URI of the UE as used in any previous request in the same dialog (In the earlier requests within the same dialog this URI appears in From header within requests sent by the UE and in To header within requests sent by the SS)
23596: 	tag
23597: A5
23598: local tag of the dialog ID (In the earlier requests within the same dialog this tag appears in From header within requests sent by the UE and in To header within requests sent by the SS)
23601: To
23605: RFC 3261 [15]
23606: 	addr-spec
23607: A6,A7
23608: emergency service URN beginning as urn:service:sos
23610: RFC 5031 [97]
23612: A20 AND (NOT A25)
23613: urn:service:sos.ecall.manual
23614: Rel-14
23615: RFC 8147 [149]
23617: A21 AND (NOT A25)
23618: urn:service:sos:ecall:automatic
23619: Rel-14
23620: RFC 8147 [149]
23622: A25
23623: The Test URI as per the generic "eCall test URI" which uses EFSDNURI from table 4.9.3.5-1 for "eCall capable" UEs or EFFDNURI from table 4.9.3.5-2 for "eCall only" UEs as specified in 3GPP TS 36.508 [94]
23624: Rel-14
23625: RFC 8147 [149]
23627: A4
23628: px_IMS_CalleeUri
23631: 	tag	
23632: A4
23633: not present
23636: 	addr-spec
23637: A5
23638: remote SIP URI of SS (i.e. the remote UE) as used in any previous request in the same dialog (In the earlier requests within the same dialog this URI appears in To header within requests sent by the UE and in From header within requests sent by the SS)
23641: 	tag	
23642: A5
23643: remote tag of the dialog ID (In the earlier requests within the same dialog this tag appears in To header within requests sent by the UE and in From header within requests sent by the SS)
23646: Call-ID
23650: RFC 3261 [15]
23651: 	callid
23652: A4
23653: value different to that received in REGISTER message
23657: A5
23658: value of Call-ID as in any previous request in the same dialog
23661: Call-Info
23662: A20,A21
23664: Rel-14
23665: RFC 8147 [149]
23666: 	cid URL
23668: any URL
23671: 	purpose
23673: emergencyCallData.eCall.MSD
23676: CSeq
23680: RFC 3261 [15]
23681: 	value
23682: A4
23683: must be present, value not checked
23687: A5
23688: value of CSeq sent by the UE within its previous request in the same dialog but increased by one
23691: 	method
23693: INVITE
23696: Supported
23698: The option tags defined below shall be included additionally to any option tags defined in any specific message content, unless specified otherwise in this specific message content.
23700: RFC 3261 [15]
23701: 	option-tag
23703: 100rel
23707: A13 OR A14
23708: norefersub
23709: Rel-11
23710: RFC 4488 [126]
23712: A4 AND A26 AND NOT (A6 OR A7 OR A19 OR A20 OR A21)
23713: timer
23715: RFC 4028 [146]
23716: P-Early-Media
23717: A16 AND (NOT A5)
23720: RFC 5009 [138]
23721: IR.92 [133]
23722: 	em-param
23724: supported
23727: Geolocation
23728: A8
23730: Rel-9
23731: RFC 6442 [98]
23732: 	locationURI
23734: cid-url indicating the Content-Id of the PIDF-LO within the multipart MIME body of INVITE request.
23735: (Note that location-by-reference URI is not allowed as the SS does not provide any external storage for location info for the UE to refer.)
23738: Geolocation-Routing
23739: A8
23740: "yes"
23741: Rel-9
23742: RFC 6442 [98]
23743: Require
23744: A1,A7
23747: RFC 3261 [15]
23749: A6
23750: not present
23753: 	option-tag
23754: A1,A7
23755: sec-agree
23757: RFC 3329 [21]
23758: Proxy-Require
23759: A1,A7
23762: RFC 3261 [15]
23763: RFC 3329 [21]
23765: A6
23766: not present
23769: 	option-tag
23770: A1,A7
23771: sec-agree
23774: Security-Verify
23775: A1,A7
23778: RFC 3329 [21]
23780: A2,A6
23781: not present
23784: 	sec-mechanism
23785: A1,A7
23786: same value as Security-Server header sent by SS
23789: Contact
23793: RFC 3261 [15]
23794: 	addr-spec
23795: (A1 OR A7) AND NOT A15
23796: SIP URI with IP address or FQDN and protected server port of UE
23800: (A2 OR A19) AND NOT A15
23801: SIP URI with IP address or FQDN and unprotected server port of UE
23805: A15 AND NOT A6
23806: Public GRUU as obtained during registration as pub-gruu contact parameter of the 200 OK for REGISTER response
23808: RFC 5627 [61]
23810: A6
23811: SIP URI with IP address and unprotected server port of UE
23814: 	c-p-instance
23815: A6
23816: +sip.instance="<urn:gsma:imei: (gsma-specifier-defined-substring)>" where gsma-specifier-defined-substring shall be the IMEI code of the UE, coded as specified in RFC 7254 [122], without optional parameters
23817: Rel-10
23818: RFC 5626 [109]
23819: RFC 7254 [122]
23821: A3,A17
23822: +g.3gpp.icsi-ref="urn%3Aurn-7%3A3gpp-service.ims.icsi.mmtel" (see NOTE 2, 4)
23825: 	feature-param
23826: A10
23827: video
23829: RFC 3840 [63]
23831: A12
23832: +g.3gpp.srvcc-alerting
23834: RFC 3840 [63]
23836: A22 AND (A23 OR A24)
23837: audio
23839: RFC 3840 [63]
23841: A18 AND NOT A5
23842: +g.3gpp.ps2cs-srvcc-orig-pre-alerting
23844: RFC 3840 [63]
23845: Max-Forwards
23849: RFC 3261 [15]
23850: 	value
23852: non-zero value
23855: P-Access-Network-Info
23856: NOT A2
23859: RFC 7315 [132]
23861: A2(o)
23862: header optional
23865: 	access-net-spec
23867: access network technology and, if applicable, the cell ID
23870: Accept
23871: NOT A5
23873: Rel-7
23874: RFC 3261 [15]
23876: A5(o)
23877: header optional
23880: 	media-range
23881: A4
23882: application/sdp,application/3gpp-ims+xml
23883: (additional medias can be added in any order)
23887: A13
23888: application/vnd.3gpp.mid-call+xml
23889: Rel-11
23892: A14
23893: application/vnd.3gpp.state-and-event-info+xml
23894: Rel-11
23897: A20,A21
23898: application/EmergencyCallData.Control+xml
23899: Rel-14
23900: RFC 8147 [149]
23901: P-Preferred-Service
23905: RFC 6050 [68]
23906: 	Service-ID
23907: A3 AND A4
23908: urn:urn-7:3gpp-service.ims.icsi.mmtel
23911: P-Preferred-Identity
23915: RFC 3325 [89]
23916: 	PPreferredID-value
23917: A7
23918: emergency public user identity (NOTE 3)
23921: Recv-Info
23925: RFC 6086 [139]
23926: 	Info-package-type
23927: A14
23928: g.3gpp.state-and-event
23932: A20,A21
23933: EmergencyCallData.eCall.MSD
23934: Rel-14
23935: RFC 8147 [149]
23936: Accept-Contact
23940: RFC 3841 [64]
23941: 	ac-value
23942: A3 AND A4
23943: +g.3gpp.icsi-ref="urn%3Aurn-7%3A3gpp-service.ims.icsi.mmtel" (see NOTE 2, 4)
23947: A10 AND A11
23948: video
23951: Proxy-Authorization
23952: A17
23955: RFC 2617 [16]
23956: RFC 3310 [17]
23957: 	username
23958: A17
23959: preconfigured in the UE
23962: 	realm
23963: A17
23964: same value as received in the realm directive in the Proxy-Authorization header sent by SS
23967: 	nonce
23968: A17
23969: same value as in Proxy-Authorization header sent by SS
23972: 	digest-uri
23973: A17
23974: preconfigured in the UE
23977: 	qop-value
23978: A17
23979: auth
23982: 	cnonce-value
23983: A17
23984: value assigned by UE affecting the response calculation
23987: 	nonce-count
23988: A17
23989: counter to indicate how many times UE has sent the same value of nonce within successive INVITESs, initial value shall be 1
23992: 	response
23993: A17
23994: response calculated by UE
23997: 	algorithm
23998: A17
23999: MD5
24002: Content-Type
24006: RFC 3261 [15]
24007: 	media-type
24008: NOT A8 AND NOT A20 AND NOT A21 AND NOT A25
24009: application/sdp
24013: A8,A20,A21
24014: A25
24015: multipart/mixed;boundary=any value
24017: RFC 6442 [98]
24018: RFC 8147 [149]
24019: Content-Length
24021: header shall be present if UE uses TCP to send this message and if there is a message body
24023: RFC 3261 [15]
24024: 	Value
24026: length of message-body
24029: Message-body
24031: consists of one or several parts as indicated by Content-Type, and each part having actual contents as follows (SDP contents, if any, is specified in dedicated sections)
24035: A8
24036: a PIDF-LO element mapped to the same Content-ID which can be found from the Geolocation header
24037: The PIDF-LO shall contain at least the following elements:
24038: -	One or more 'geopriv' elements, each containing:
24039: -	One 'location-info' element describing the location of the UE; and
24040: -	One 'usage-rules' element describing the limitations of the usage of the location info
24044: (A20 OR A21) AND NOT A25
24045: --boundary value (as provided in SIP hdr Content-Type)
24046: Content-Type: application/EmergencyCallData.eCall.MSD
24047: Content-ID: same URL as in Call-Info header
24048: Content-Disposition: by-reference;handling=optional
24049: MSD in ASN.1 PER encoding
24050: --boundary value (as provided in SIP hdr Content-Type)
24051: Rel-14
24052: RFC 8147 [149]
24054: Condition
24055: Explanation
24056: A1
24057: IMS security (A.6a/2 3GPP TS 34.229-2 [5])
24058: A2
24059: GIBA (A.6a/1 3GPP TS 34.229-2 [5])
24060: A3
24061: UE supports MTSI (A.3A/50 3GPP TS 34.229-2 [5])
24062: A4
24063: INVITE creating a dialog
24064: A5
24065: re-INVITE within a dialog
24066: A6
24067: INVITE for creating an emergency session in case of no registration
24068: A7
24069: INVITE for creating an emergency session within an emergency registration using IMS security
24070: A8
24071: UE is capable of obtaining location information, has obtained its location and is setting up an emergency session
24072: A9
24073: Void
24074: A10
24075: UE supports video feature tag (A.12/32 3GPP TS 34.229-2 [5])
24076: A11
24077: INVITE for creating a video call
24078: A12
24079: INVITE for creating a voice or video call and UE supports g.3gpp.srvcc-alerting media feature tag (A.12/34 3GPP TS 34.229-2 [5])
24080: A13
24081: INVITE for creating a voice call during rSRVCC and UE CS to PS SRVCC with the MSC assisted mid-call feature (A.12/42 3GPP TS 34.229-2 [5])
24082: A14
24083: INVITE for creating a voice call and UE supports CS to PS SRVCC for calls in alerting phase (A.12/41 3GPP TS 34.229-2 [5])
24084: A15
24085: obtaining and using GRUUs in the Session Initiation Protocol (SIP) (A.4/53 3GPP TS 34.229-2 [5])
24086: A16
24087: UE supports early media (A.12/45 3GPP TS 34.229-2 [5])
24088: A17
24089: SIP Digest without TLS for Fixed Broadband Access (SIP Digest without TLS, A.6a/5 3GPP TS 34.229-2 [5])
24090: A18
24091: UE indicates g.3gpp.ps2cs-srvcc-orig-pre-alerting media feature tag in INVITE request (A.12/36 3GPP TS 34.229-2 [5])
24092: A19
24093: INVITE for creating an emergency session within an emergency registration using GIBA
24094: A20
24095: INVITE for creating an eCall over IMS session manually
24096: A21
24097: INVITE for creating an eCall over IMS session automatically
24098: A22
24099: UE supports audio media feature tag (A.12/56 3GPP TS 34.229-2 [5])
24100: A23
24101: UE uses E-UTRAN access and has received IMS voice over PS Session Supported Indication in the NAS ATTACH ACCEPT message as described in TS 24.301 [150], clauses 8.2.1 and 9.9.3.12A
24102: A24
24103: UE uses UTRAN/GERAN access and has received IMS voice over PS Session Supported Indication in the NAS ATTACH ACCEPT message as described in TS 24.008 [12], clauses 9.4.2 and 10.5.5.23
24104: A25
24105: INVITE for creating a test eCall over IMS session
24106: A26
24107: UE supports Session Timer (A.12/57 3GPP TS 34.229-2 [5])
24109: NOTE 1:	All choices for applicable conditions are described for each header.
24110: NOTE 2:	The "=" may include optional linear white spaces according to the EQUAL definition in chapter 25.1, RFC 3261 [15].
24111: NOTE 3:	According to TS 24.229 clause 5.1.1.1A and 5.1.6.2 [10] when the UE is using ISIM the emergency public user identity is the first public user identity in the list stored in the ISIM; when there is no ISIM it is the default public user id if the UE registered or the temporary user id (derived from IMSI) else.
24112: NOTE 4:	URN is the outcome of URL encoding ("Percent-Encoding" according to RFC 3986 [129]) of urn:urn-7:3gpp-service.ims.icsi.mmtel.
```

## A.2.3 183 Session Progress for INVITE（行 24220-24496；used_by: TC-012, TC-019）

关键官方标记：`183`、`Session Progress`、`Require`、`Supported`、`Content-Type`

```text
24220: A.2.3	183 Session Progress for INVITE
24221: Header/param
24222: Cond
24223: Value/remark
24224: Rel
24225: Reference
24226: Status-Line
24230: RFC 3261 [15]
24231: 	SIP-Version
24233: SIP/2.0
24236: 	Status-Code
24238: 183
24241: 	Reason-Phrase
24243: Session Progress
24246: Record-Route
24248: order of the parameters in this header must be like in the respective rows
24250: RFC 3261 [15]
24251: 	rec-route
24252: A1
24253: <sip:pcscf.other.com;lr>, <sip:scscf.other.com;lr>, <sip:orig@scscf.3gpp.org;lr>, <sip:SS P-CSCF address: protected server port of SS;lr>
24256: 	rec-route
24258: A3
24259: <sip:pcscf.other.com;lr>, <sip:scscf.other.com;lr>, <sip:orig@scscf.3gpp.org;lr>, <sip:SS P-CSCF address: unprotected server port of SS (optional);lr>
24262: 	rec-route
24263: A2
24264: same value as received in INVITE
24267: 	rec-route
24268: A4
24269: same value as received in INVITE
24272: 	rec-route
24273: A5
24274: <sip:orig@ecscf.other.com;lr>, <sip:SS P-CSCF address:protected server port of SS;lr>
24277: Via
24281: RFC 3261 [15]
24282: 	via-parm
24284: same value as received in INVITE message
24287: Require
24289: The option tags defined below shall be included additionally to any option tags defined in any specific message content, unless specified otherwise in this specific message content.
24291: RFC 3261 [15]
24292: 	option-tag	
24294: 100rel
24297: From
24301: RFC 3261 [15]
24302: 	addr-spec
24304: same value as received in INVITE message
24307: 	tag
24309: same value as received in INVITE message
24312: To
24316: RFC 3261 [15]
24317: 	addr-spec
24319: same value as received in INVITE message
24322: 	tag
24323: A1, A3, A5, A6
24324: common to-tag (invite)
24327: 	tag
24328: A2, A4
24329: any value
24332: P-Asserted-Identity
24333: A5
24336: RFC 3325 [89]
24337: 	addr-spec
24339: A tel URI that can be recognized as valid emergency numbers if dialled by the user are specified in 3GPP TS 22.101 [39]. The emergency numbers 112 and 911 are stored on the ME, in accordance with 3GPP TS 22.101 [39]
24342: 	uri-parameter
24344: lr
24347: Contact
24351: RFC 3261 [15]
24352: RFC 5627 [61]
24353: 	addr-spec 
24354: A1, A3
24355: px_IMS_CalleeContactUri
24358: 	addr-spec 
24359: A2 AND NOT A9
24360: SIP URI with IP address or FQDN and protected server port of UE
24363: 	addr-spec
24364: A4 AND NOT A9
24365: SIP URI with IP address or FQDN and unprotected server port of UE
24368: 	addr-spec
24369: A2 AND A9
24370: Public GRUU as obtained during registration as pub-gruu contact parameter of the 200 OK for REGISTER response
24373: 	addr-spec
24374: A4 AND A9
24375: Public GRUU as obtained during registration as pub-gruu contact parameter of the 200 OK for REGISTER response
24378: 	feature-param
24380: +g.3gpp.icsi-ref="urn%3Aurn-7%3A3gpp-service.ims.icsi.mmtel"(see NOTE 2, 3)
24383: 	feature-param
24384: A6
24385: video
24388: 	feature-param
24389: A10
24390: audio
24393: 	feature-param
24394: A11 AND A12 AND (A13 OR A14)
24395: audio
24399: Rseq
24403: RFC 3262 [33]
24404: 	response-num
24405: A2, A4
24406: any value
24409: 	response-num
24410: A1, A3
24411: 121 (arbitrarily selected)
24414: Call-ID
24418: RFC 3261 [15]
24419: 	callid
24421: same value as received in INVITE message
24424: CSeq
24428: RFC 3261 [15]
24429: 	value
24431: same value as received in INVITE message
24434: Feature-Caps	feature-param
24436: A8
24438: +g.3gpp.ps2cs-srvcc-orig-pre-alerting
24440: RFC 6809 [125]
24441: TS 24.237 [110]
24442: Content-Type
24446: RFC 3261 [15]
24447: 	media-type
24449: application/sdp
24452: Content-Length
24453: A1, A3
24456: RFC 3261 [15]
24457: 	value
24459: length of message-body
24463: Condition
24464: Explanation
24465: A1
24466: 183 sent by the SS (IMS security, A.6a/2 3GPP TS 34.229-2 [5])
24467: A2
24468: 183 sent by the UE (IMS security, A.6a/2 3GPP TS 34.229-2 [5])
24469: A3
24470: 183 sent by the SS (GIBA, A.6a/1 3GPP TS 34.229-2 [5])
24471: A4
24472: 183 sent by the UE (GIBA, A.6a/1 3GPP TS 34.229-2 [5])
24473: A5
24474: 183 sent by the SS for INVITE for a non-UE detectable emergency call
24475: A6
24476: UE supports video media feature tag (A.12/32 3GPP TS 34.229-2 [5])
24477: A7
24478: Void
24479: A8
24480: 183 sent by the SS for a voice call and UE supports pre-alerting media feature tag (A.12/36 3GPP TS 34.229-2 [5])
24481: A9
24482: obtaining and using GRUUs in the Session Initiation Protocol (SIP) (A.4/53 3GPP TS 34.229-2 [5])
24483: A10
24484: Void
24485: A11
24486: Void
24487: A12
24488: UE supports audio media feature tag (A.12/56 3GPP TS 34.229-2 [5])
24489: A13
24490: UE uses E-UTRAN access and has received IMS voice over PS Session Supported Indication in the NAS ATTACH ACCEPT message as described in TS 24.301 [150], clauses 8.2.1 and 9.9.3.12A.
24491: A14
24492: UE uses UTRAN/GERAN access and has received IMS voice over PS Session Supported Indication in the NAS ATTACH ACCEPT message as described in TS 24.008 [12], clauses 9.4.2 and 10.5.5.23.
24494: NOTE1:	All choices for applicable conditions are described for each header.
24495: NOTE 2:	The "=" may include optional linear white spaces according to the EQUAL definition in chapter 25.1, RFC 3261 [15].
24496: NOTE 3:	URN is the outcome of the URL encoding ("Percent-Encoding" according to RFC 3986 [129]) of urn:urn-7:3gpp-service.ims.icsi.mmtel. 
```

## A.2.6 180 Ringing for INVITE（行 24966-25209；used_by: TC-012, TC-019）

关键官方标记：`180`、`Ringing`、`Contact`

```text
24966: A.2.6	180 Ringing for INVITE
24967: Header/param
24968: Cond
24969: Value/remark
24970: Rel
24971: Reference
24972: Status-Line
24976: RFC 3261 [15]
24977: 	SIP-Version
24979: SIP/2.0
24982: 	Status-Code
24984: 180
24987: 	Reason-Phrase
24989: Ringing
24992: Record-Route
24996: RFC 3261 [15]
24997: 	rec-route
24999: as defined for the common 183 response, see A.2.3
25002: 	rec-route
25003: A7
25004: <sip:orig@ecscf.other.com;lr>, <sip:SS P-CSCF address:unprotected server port of SS;lr>
25007: 	rec-route
25008: A8
25009: <sip:orig@ecscf.other.com;lr>, <sip:SS P-CSCF address:protected server port of SS;lr>
25012: Via
25016: RFC 3261 [15]
25017: 	via-parm
25019: same value as received in INVITE message
25022: Require
25024: The option tags defined below shall be included additionally to any option tags defined in any specific message content, unless specified otherwise in this specific message content.
25026: RFC 3261 [15]
25027: 	option-tag	
25028: A3
25029: 100rel
25032: From
25036: RFC 3261 [15]
25037: 	addr-spec
25039: same value as received in INVITE message
25042: 	tag
25044: same value as received in INVITE message
25047: To
25051: RFC 3261 [15]
25052: 	addr-spec
25054: same value as received in INVITE message
25057: 	tag	
25059: as defined for the common 183 response, see A.2.3
25062: P-Asserted-Identity
25063: A4
25066: RFC 3325 [89]
25067: 	addr-spec
25069: A tel URI that can be recognized as valid emergency numbers if dialled by the user are specified in 3GPP TS 22.101 [39]. The emergency numbers 112 and 911 are stored on the ME, in accordance with 3GPP TS 22.101 [39]
25072: 	uri-parameter
25074: lr
25077: Contact
25081: RFC 3261 [15]
25082: 	addr-spec
25084: as defined for the common 183 response, see A.2.3
25087: 	feature-param
25088: A5
25089: +g.3gpp.srvcc-alerting
25092: 	feature-param
25093: A1
25094: audio
25097: 	feature-param
25098: A2 AND A9 AND (A10 OR A11)
25099: audio
25102: Rseq
25106: RFC 3262 [33]
25107: 	response-num
25108: A3 AND NOT A12
25109: previous RSeq number sent in the same direction incremented by one
25112: 	response-num
25113: A1 AND A12
25114: 122
25117: 	response-num
25118: A2 AND A12
25119: any value
25122: Call-ID
25126: RFC 3261 [15]
25127: 	callid
25129: same value as received in INVITE message
25132: CSeq
25136: RFC 3261 [15]
25137: 	value
25139: same value as received in INVITE message
25142: P-Access-Network-Info
25147: 	access-net-spec
25148: A2
25149: access network technology and, if applicable, the cell ID
25152: P-Access-Network-Info
25153: A1
25154: not present
25157: 	access-net-spec
25162: Feature-Caps
25167: 	feature-param
25168: A6
25169: +g.3gpp.srvcc-alerting
25172: Content-Length
25173: A1
25176: RFC 3261 [15]
25177: 	value
25179: length of message-body
25183: Condition
25184: Explanation
25185: A1
25186: 180 sent by the SS
25187: A2
25188: 180 sent by the UE
25189: A3
25190: Response sent reliably (e.g. always when it contains an SDP body)
25191: A4
25192: 180 sent by the SS when setting up an emergency call or a non-UE detectable emergency call
25193: A5
25194: 180 sent by the UE for a voice or video call and UE supports g.3gpp.srvcc-alerting media feature tag (A.12/34 3GPP TS 34.229-2 [5])
25195: A6
25196: 180 sent by the SS for a voice or video call and UE supports g.3gpp.srvcc-alerting media feature tag (A.12/34 3GPP TS 34.229-2 [5])
25197: A7
25198: Response sent by SS for emergency call without emergency registration
25199: A8
25200: Response sent by SS for emergency call with emergency registration or a non-UE detectable emergency call
25201: A9
25202: UE supports audio media feature tag (A.12/56 3GPP TS 34.229-2 [5])
25203: A10
25204: UE uses E-UTRAN access and has received IMS voice over PS Session Supported Indication in the NAS ATTACH ACCEPT message as described in TS 24.301 [150], clauses 8.2.1 and 9.9.3.12A.
25205: A11
25206: UE uses UTRAN/GERAN access and has received IMS voice over PS Session Supported Indication in the NAS ATTACH ACCEPT message as described in TS 24.008 [12], clauses 9.4.2 and 10.5.5.23.
25207: A12
25208: 180 Ringing is first provisional response sent reliably in this dialog
```

## A.2.7 ACK（行 25210-25387；used_by: TC-012, TC-019, TC-020）

关键官方标记：`ACK`、`Request-URI`、`CSeq`

```text
25210: A.2.7	ACK
25211: Header/param
25212: Cond
25213: Value/remark
25214: Rel
25215: Reference
25216: Request-Line
25220: RFC 3261 [15]
25221: 	Method
25223: ACK
25226: 	Request-URI
25228: A4
25229: same value as in PRACK message
25230: same value as in INVITE message
25233: 	SIP-Version
25235: SIP/2.0
25238: Via
25242: RFC 3261 [15]
25243: 	sent-protocol
25244: A1
25245: SIP/2.0/UDP (when using UDP) or
25246: SIP/2.0/TCP (when using TCP)
25250: A2
25251: same as in INVITE
25254: 	sent-by
25256: same value as in INVITE message
25259: 	via-branch	
25260: A3
25261: value starting with 'z9hG4bk'
25264:      via-branch
25265: A4
25266: Same value as received in INVITE
25269: Route
25273: RFC 3261 [15]
25274: 	route-param
25275: A1 AND A3 AND (NOT A5)
25276: URIs of the Record-Route header sent to the UE in 183, 180 or 200 response (whichever response used for INVITE to be acknowledged and contained Record-Route header) in reverse order
25280: A1 AND A4 AND (NOT A5)
25281: Contents shall be the same as Route header sent in INVITE
25285: A1 AND A5
25286: Contents shall be the same as Route header in re-INVITE
25289: From
25293: RFC 3261 [15]
25294: 	addr-spec
25295: A1
25296: SIP URI of the UE as received in INVITE.
25300: A2
25301: SIP URI of the SS as sent in INVITE
25304: 	tag
25306: local tag of the dialog ID (same as from-tag in the INVITE message)
25309: To
25313: RFC 3261 [15]
25314: 	addr-spec
25315: A1
25316: SIP URI of the SS as received in INVITE.
25320: A2
25321: SIP URI of the UE as sent in INVITE
25324: 	tag	
25326: remote tag of the dialog ID (as chosen in an earlier response of the dialog)
25329: Call-ID
25333: RFC 3261 [15]
25334: 	callid
25336: same value as in INVITE message
25339: CSeq
25343: RFC 3261 [15]
25344: 	value
25346: same value as in INVITE message
25349: 	method
25351: ACK
25354: Max-Forwards
25358: RFC 3261 [15]
25359: 	value
25361: non-zero value
25364: Content-Length
25365: A2
25368: RFC 3261 [15]
25369: 	value
25371: 0
25375: Condition
25376: Explanation
25377: A1
25378: ACK sent by the UE
25379: A2
25380: ACK sent by the SS
25381: A3
25382: ACK for 2xx response
25383: A4
25384: ACK for non-2xx response
25385: A5
25386: ACK for re-INVITE
```

## A.2.8 BYE（行 25388-25667；used_by: TC-012, TC-019, TC-020, TC-021）

关键官方标记：`BYE`、`CSeq`、`Max-Forwards`、`Content-Length`

```text
25388: A.2.8	BYE
25389: Header/param
25390: Cond
25391: Value/remark
25392: Rel
25393: Reference
25394: Request-Line
25398: RFC 3261 [15]
25399: 	Method
25401: BYE
25404: 	Request-URI
25406: same URI value as the recipient of BYE has earlier sent in its Contact header within the same dialog
25409: 	SIP-Version
25411: SIP/2.0
25414: Via
25418: RFC 3261 [15]
25419: 	sent-protocol
25421: SIP/2.0/UDP (when using UDP) or
25422: SIP/2.0/TCP (when using TCP)
25425: 	sent-by
25426: A1, A2
25427: MO Call has been established:
25428: same value as in INVITE message
25429: MT Call has been established:
25430: same value as defined in A.2.1
25431: (IP address or FQDN)
25435: A3, A4
25436: same values as defined in A.2.9
25437: (There is more than one value)
25440: 	via-branch
25442: value starting with 'z9hG4bK' (NOTE 2)
25445: Route
25449: RFC 3261 [15]
25450: 	route-param
25451: A1, A2
25452: MO Call has been established:
25453: URIs of the Record-Route header of 183 response in reverse order (or any other response creating the dialog according to RFC 3261 clause 12.1 [15])
25454: MT Call has been established:
25455: value of Record-Route header as defined in A.2.9
25458: Route
25459: A3, A4
25460: not present
25463: From
25467: RFC 3261 [15]
25468: 	addr-spec
25470: SIP URI of the UE when BYE is sent by the UE.
25471: SIP URI of the SS when BYE is sent by the SS.
25472: URI must be the same as used for the endpoint in the earlier requests within the dialog.
25475: 	tag
25477: local tag of the dialog ID
25480: To
25484: RFC 3261 [15]
25485: 	addr-spec
25487: SIP URI of the SS when BYE is sent by the UE.
25488: SIP URI of the UE when BYE is sent by the SS.
25489: URI must be the same as used for the endpoint in the earlier requests within the dialog.
25492: 	tag	
25494: remote tag of the dialog ID
25497: Call-ID
25501: RFC 3261 [15]
25502: 	callid
25504: same value as sent or received in INVITE message
25507: CSeq
25511: RFC 3261 [15]
25512: 	value
25514: value of CSeq sent by the endpoint within its previous request in the same dialog but increased by one
25517: 	method
25519: BYE
25522: Require
25523: (A1 OR A5) AND NOT A6
25526: RFC 3261 [15]
25527: RFC 3329 [21]
25528: 	option-tag
25529: A1, A5
25530: sec-agree
25533: Require
25534: A2, A6
25535: not present
25538: Proxy-Require
25539: (A1 OR A5) AND NOT A6
25542: RFC 3261 [15]
25543: RFC 3329 [21]
25544: 	option-tag
25545: A1, A5
25546: sec-agree
25549: Proxy-Require
25550: A2, A6
25551: not present
25554: Security-Verify
25555: (A1 OR A5) AND NOT A6
25558: RFC 3329 [21]
25559: 	sec-mechanism
25560: A1, A5
25561: same value as Security-Server header sent by SS
25564: Security-Verify
25565: A2, A6
25566: not present
25569: Max-Forwards
25573: RFC 3261 [15]
25574: 	value
25576: non-zero value
25579: P-Access-Network-Info
25580: A1, A2(o)
25583: RFC 7315 [132]
25584: 	access-net-spec
25586: access network technology and, if applicable, the cell ID
25589: Proxy-Authorization
25590: A5
25593: RFC 2617 [16]
25594: RFC 3310 [17]
25595: 	username
25596: A5
25597: preconfigured in the UE
25600: 	realm
25601: A5
25602: same value as received in the realm directive in the Proxy-Authorization header sent by SS
25605: 	nonce
25606: A5
25607: same value as in Proxy-Authorization header sent by SS
25610: 	digest-uri
25611: A5
25612: preconfigured in the UE
25615: 	qop-value
25616: A5
25617: auth
25620: 	cnonce-value
25621: A5
25622: value assigned by UE affecting the response calculation
25625: 	nonce-count
25626: A5
25627: counter to indicate how many times UE has sent the same value of nonce within successive INVITESs, initial value shall be 1
25630: 	response
25631: A5
25632: response calculated by UE
25635: 	algorithm
25636: A5
25637: MD5
25640: Content-Length
25641: A3, A4
25644: RFC 3261 [15]
25645: 	value
25647: length of message body
25651: Condition
25652: Explanation
25653: A1
25654: BYE sent by the UE (IMS security, A.6a/2 3GPP TS 34.229-2 [5])
25655: A2
25656: BYE sent by the UE (GIBA, A.6a/1 3GPP TS 34.229-2 [5])
25657: A3
25658: BYE sent by the SS (IMS security, A.6a/2 3GPP TS 34.229-2 [5])
25659: A4
25660: BYE sent by the SS (GIBA, A.6a/1 3GPP TS 34.229-2 [5])
25661: A5
25662: SIP Digest without TLS for Fixed Broadband Access (SIP Digest without TLS, A.6a/5 3GPP TS 34.229-2 [5])
25663: A6
25664: BYE for emergency call with no registration
25666: NOTE 1:	All choices for applicable conditions are described for each header.
25667: NOTE 2:	Branch parameter values sent by SS are different within a test case execution.
```

## A.2.9 INVITE for MT Call（行 25668-26027；used_by: TC-019）

关键官方标记：`INVITE`、`P-Called-Party-ID`、`Accept-Contact`、`Request-URI`

```text
25668: A.2.9	INVITE for MT Call
25669: Header/param
25670: Cond
25671: Value/remark
25672: Rel
25673: Reference
25674: Request-Line
25678: RFC 3261 [15]
25679: 	Method
25681: INVITE
25684: 	Request-URI
25685: A4
25686: UE's registered contact address in SIP URI form, as provided in the Contact header of the REGISTER message
25689: 	Request-URI
25690: A5
25691: UE's contact address in SIP URI form, as provided in the Contact header within any response or request within the dialog
25694: 	Request-URI
25695: A10
25696: UE's registered contact address in SIP URI form, as provided in the Contact header of the REGISTER message with the tag user = phone
25699: 	SIP-Version
25701: SIP/2.0
25704: Via
25708: RFC 3261 [15]
25709: 	sent-protocol
25711: SIP/2.0/UDP (when using UDP) or 
25712: SIP/2.0/TCP (when using TCP)
25715: 	sent-by
25716: A1
25717:  The SS P-CSCF address and the SS protected server port 
25720: 	sent-by
25721: A2
25722: The SS P-CSCF address and the SS unprotected server port (optional)
25725: 	via-branch	
25727: Value starting with 'z9hG4bK'
25730: Via
25732: In addition to the via-parm entry for the SS, the following via-parm entries are included:
25734: RFC 3261 [15]
25735: 	via-parm
25737: SIP/2.0/UDP scscf1.3gpp.org;branch=z9hG4bK..., SIP/2.0/UDP scscf2.3gpp.org;branch=z9hG4bK..., SIP/2.0/UDP pcscf2.3gpp.org;branch=z9hG4bK...,
25738: SIP/2.0/UDP caller.3gpp.org:6543;branch=z9hG4bK... 
25739: (NOTE 3)
25742: Record-Route
25746: RFC 3261 [15]
25747: 	rec-route
25748: A1 AND A4
25749: <sip: SS P-CSCF address: protected server port of SS ;lr>
25752: 	rec-route
25753: A2 AND A4
25754:  <sip: SS P-CSCF address SS unprotected server port (optional);lr>
25757: Record-Route
25759: In addition to the rec-route entry for the SS, the following rec-route entries are included:
25761: RFC 3261 [15]
25762: 	rec-route
25764: <sip:term@scscf1.3gpp.org;lr>, <sip:orig@scscf2.3gpp.org;lr>, <sip:pcscf2.3gpp.org;lr>
25767: Record-Route
25768: 	rec-route
25770: A1 AND A5
25772: MO call established: 
25773: same value as in 183 Session Progress for INVITE, condition A1, in reverse order
25774: MT call established: 
25775: <sip: SS P-CSCF address: protected server port of SS ;lr>
25777: RFC 3261 [15]
25778: Record-Route
25779: 	rec-route
25781: A2 AND A5
25783: MO call established: 
25784: same value as in 183 Session Progress for INVITE, condition A3, in reverse order
25785: MT call established:
25786: <sip: SS P-CSCF address SS unprotected server port (optional);lr>
25788: RFC 3261 [15]
25789: From
25793: RFC 3261 [15]
25794: 	addr-spec
25795: A4
25796: SIP URI of the SS representing the calling UE
25799: 	tag
25800: A4
25801: any value 
25804: 	addr-spec
25805: A5
25806: SIP URI of the SS representing the calling UE as used in any previous request in the same dialog (In the earlier requests within the same dialog this URI appears in To header within requests sent by the UE and in From header within requests sent by the SS)
25809: 	tag
25810: A5
25811: local tag of the dialog ID 
25814: To
25818: RFC 3261 [15]
25819: 	addr-spec
25820: A4
25821: SIP URI of the UE's default public user id
25824: 	tag	
25825: A4
25826: not present
25829: 	addr-spec
25830: A5
25831: SIP URI of the UE as used in any previous request in the same dialog (In the earlier requests within the same dialog this URI appears in From header within requests sent by the UE and in To header within requests sent by the SS)
25834: 	tag
25835: A5
25836: remote tag of the dialog ID 
25839: Call-ID
25843: RFC 3261 [15]
25844: 	callid
25845: A4
25846: a random text string generated by the SS
25849: 	callid
25850: A5
25851: value of Call-ID as in any previous request in the same dialog
25854: CSeq
25858: RFC 3261 [15]
25859: 	value
25860: A4
25861: any value (e.g. 4711)
25864: 	value
25865: A5
25866: value of CSeq sent by the SS within its previous request in the same dialog but increased by one
25869: 	method
25871: INVITE
25874: Supported
25876: The option tags defined below shall be included additionally to any option tags defined in any specific message content, unless specified otherwise in this specific message content.
25878: RFC 3261 [15]
25879: 	option-tag
25881: 100rel
25884: 	option-tag
25886: timer
25888: RFC 4028 [146]
25889: P-Called-Party-ID
25891: One of the UE's registered, non-barred public ID
25893: RFC 7315 [132]
25894: Contact
25898: RFC 3261 [15]
25899: 	addr-spec
25900: A1
25901: SIP URI with IP address or FQDN and protected server port of the calling UE, for example "sip:caller@3gpp.org:6543"
25904: 	addr-spec
25905: A2
25906: SIP URI with IP address or FQDN and unprotected server port of the calling UE
25909: 	addr-spec
25910: A5
25911: same contact information for the SS as used before in this dialog
25914: 	feature-param
25915: A3
25916: +g.3gpp.icsi-ref="urn%3Aurn-7%3A3gpp-service.ims.icsi.mmtel" (NOTE 2)
25919: 	feature-param
25920: 	feature-param
25921: A7
25922: video 
25923: audio
25926: Content-Type
25930: RFC 3261 [15]
25931: 	media-type
25933: application/sdp
25936: Max-Forwards
25940: RFC 3261 [15]
25941: 	value
25943: non-zero value
25946: Accept
25949: Rel-7
25950: RFC 3261 [15]
25951:       media-range
25952: A4
25953: application/sdp, application/3gpp-ims+xml
25956: P-Asserted-Service
25960: RFC 6050 [68]
25961:      Service-ID
25962: A3 AND A4
25963: urn:urn-7:3gpp-service.ims.icsi.mmtel
25966: Accept-Contact
25970: RFC 3841 [64]
25971:      ac-value
25972: A3 AND A4
25973: *;+g.3gpp.icsi-ref="urn%3Aurn-7%3A3gpp-service.ims.icsi.mmtel" (NOTE 2)
25976:      ac-value
25977: A8
25978: video
25981: Content-Length
25985: RFC 3261 [15]
25986: 	value
25988: length of message-body
25991: Feature-Caps
25996: 	feature-param
25997: A9
25998: g.3gpp.srvcc-alerting
26002: Condition
26003: Explanation
26004: A1
26005: IMS security (A.6a/2 3GPP TS 34.229-2 [5])
26006: A2
26007: GIBA (A.6a/1 3GPP TS 34.229-2 [5])
26008: A3
26009: UE supports MTSI (A.3A/50 3GPP TS 34.229-2 [5])
26010: A4
26011: INVITE creating a dialog
26012: A5
26013: re-INVITE within a dialog
26014: A6
26015: Void
26016: A7
26017: UE supports video feature tag (A.12/32 3GPP TS 34.229-2 [5])
26018: A8
26019: INVITE for creating a video call and UE supports video media feature tag (A.12/32 3GPP TS 34.229-2 [5])
26020: A9
26021: INVITE for creating a voice or video call and UE supports g.3gpp.srvcc-alerting media feature tag (A.12/34 3GPP TS 34.229-2 [5])
26022: A10
26023: SIP Digest without TLS for Fixed Broadband Access (SIP Digest without TLS, A.6a/5 3GPP TS 34.229-2 [5])
26025: NOTE1:	All choices for applicable conditions are described for each header.
26026: NOTE 2:	URN is the outcome of the URL encoding ("Percent-Encoding" according to RFC 3986 [129]) of urn:urn-7:3gpp-service.ims.icsi.mmtel.
26027: NOTE 3:	Branch parameter values sent by SS are different within a test case execution.
```

## A.2.10 MO REFER（行 26028-26269；used_by: TC-021）

关键官方标记：`REFER`、`Refer-To`、`Request-URI`、`CSeq`

```text
26028: A.2.10	MO REFER
26029: Header/param
26030: Cond
26031: Value/remark
26032: Rel
26033: Reference
26034: Request-Line
26038: RFC 3261 [15]
26039: 	Method
26041: REFER
26044: 	Request-URI
26046: same URI value as the SS has earlier sent in its Contact header within the same dialog
26049: 	SIP-Version
26051: SIP/2.0
26054: Via
26058: RFC 3261 [15]
26059: 	sent-protocol
26061: SIP/2.0/UDP (when using UDP) or 
26062: SIP/2.0/TCP (when using TCP)
26065: 	sent-by
26066: A1
26067: IP address or FQDN and protected server port of the UE
26071: A2
26072: IP address or FQDN and unprotected server port of the UE
26075: 	via-branch	
26077: value starting with 'z9hG4bK'
26080: Route
26082: order of the parameters in this header must be like in this table
26084: RFC 3261 [15]
26085: 	route-param
26086: A1
26087: URIs of the Record-Route header of 183 response in reverse order
26091: A2
26092: URIs of the Record-Route header of 183 response in reverse order
26095: From
26099: RFC 3261 [15]
26100: 	addr-spec
26102: local SIP URI of the UE which must be the same URI as used for the UE in the earlier requests within the dialog
26105: 	tag
26107: local tag of the dialog ID
26110: To
26114: RFC 3261 [15]
26115: 	addr-spec
26117: SIP URI of the SS which must be the same URI as used for the UE in the earlier requests within the dialog
26120: 	tag	
26122: remote tag of the dialog ID
26125: Call-ID
26129: RFC 3261 [15]
26130: 	callid
26132: same value as in the first INVITE during the call setup
26135: CSeq
26139: RFC 3261 [15]
26140: 	value
26142: value of CSeq sent by the UE within its previous request in the same dialog but increased by one
26145: 	method
26147: REFER
26150: Require
26151: A1
26154: RFC 3261 [15]
26155: RFC 3312 [31]
26156: RFC 3329 [21]
26157: 	option-tag
26159: sec-agree
26167: Proxy-Require
26168: A1
26171: RFC 3261 [15]
26172: RFC 3329 [21]
26173: 	option-tag
26175: sec-agree
26178: Security-Verify
26179: A1
26182: RFC 3329 [21]
26183: 	sec-mechanism
26185: same value as Security Server header sent by SS
26188: Security-Verify
26189: A2
26190: not present
26192: RFC 3329 [21]
26193: 	sec-mechanism
26198: Contact
26202: RFC 3261 [15]
26203: RFC 5627 [61]
26204: 	addr-spec
26205: A1
26206: SIP URI with IP address or FQDN and protected server port of UE
26210: A2
26211: SIP URI with IP address or FQDN and unprotected server port of UE
26215: A3
26216: Public GRUU as obtained during registration as pub-gruu contact parameter of the 200 OK for REGISTER response
26219: Refer-To
26223: RFC 3515 [72]
26224: 	addr-spec
26226: SIP or Tel URI of the transfer target (Note 1)
26229: Max-Forwards
26233: RFC 3261 [15]
26234: 	value
26236: non-zero value
26239: P-Access-Network-Info
26240: A1, A2(o)
26243: RFC 7315 [132]
26244: 	access-net-spec
26246: access network technology and, if applicable, the cell ID
26249: Content-Length
26251: header shall be present if UE uses TCP to send this request and if there is a message-body
26253: RFC 3261 [15]
26254: 	value
26256: length of message-body
26259: Note 1:	The SIP URI may contain a "Replaces" header referring to the dialog ID which has been established before.
26261: Condition
26262: Explanation
26263: A1
26264: IMS security (A.6a/2 3GPP TS 34.229-2 [5])
26265: A2
26266: GIBA (A.6a/1 3GPP TS 34.229-2 [5])
26267: A3
26268: obtaining and using GRUUs in the Session Initiation Protocol (SIP) (A.4/53 3GPP TS 34.229-2 [5])
```

## A.2.11 MT NOTIFY for refer package（行 26270-26476；used_by: TC-021）

关键官方标记：`NOTIFY`、`Event`、`refer`、`Subscription-State`、`message/sipfrag`

```text
26270: A.2.11	MT NOTIFY for refer package
26271: Header/param
26272: Cond
26273: Value/remark
26274: Rel
26275: Reference
26276: Request-Line
26280: RFC 3261 [15]
26281: 	Method
26283: NOTIFY
26286: 	Request-URI
26288: same URI value which the UE sent in its Contact header within the REFER request
26291: 	SIP-Version
26293: SIP/2.0
26296: Via
26298: order of the parameters in this header must be like in this table
26300: RFC 3261 [15]
26301: 	via-parm1:
26306: 		Sent-protocol
26308: SIP/2.0/UDP  when using UDP or SIP/2.0/TCP  when using TCP
26311: 		sent-by
26312: A1
26313: IP address and protected server port of SS
26316: 		sent-by
26317: A2
26318: IP address and unprotected server port of SS (optional)
26321: 		via-branch
26323: value starting with 'z9hG4bK' (NOTE 1)
26326: 	via-parm2:
26328: In addition to the via-parm entry for the SS, the following via-parm entries are included:
26331: 	via-parm
26333: SIP/2.0/UDP scscf1.3gpp.org;branch=z9hG4bK..., SIP/2.0/UDP scscf2.3gpp.org;branch=z9hG4bK..., SIP/2.0/UDP pcscf2.3gpp.org;branch=z9hG4bK...,
26334: SIP/2.0/UDP uas.3gpp.org:6543;branch=z9hG4bK...
26336: (NOTE 1)
26339: From
26343: RFC 3261 [15]
26344: 	addr-spec
26346: SIP URI of the SS which must be the same URI as used for the SS in the earlier requests within the dialog
26349: 	tag
26351: local tag of the dialog ID
26354: To
26358: RFC 3261 [15]
26359: 	addr-spec
26361: SIP URI of the UE which must be the same as used for the UE in the earlier requests within the dialog.
26364: 	tag	
26366: remote tag of the dialog ID 
26369: Call-ID
26373: RFC 3261 [15]
26374: 	callid
26376: same value as in the INVITE (and REFER) message
26379: CSeq
26380: A1,A2
26383: RFC 3261 [15]
26384: 	value
26386: value of CSeq sent by the SS within its previous request in the same dialog but increased by one
26389: 	method
26391: NOTIFY
26394: Contact
26398: RFC 3261 [15]
26399: 	addr-spec
26400: A1
26401: SIP URI with IP address or FQDN and protected server port of the SS (transferee)
26404: 	addr-spec
26405: A2
26406: SIP URI with IP address or FQDN and unprotected server port of the SS (transferee)
26409: Content-Type
26413: RFC 3261 [15]
26414: RFC 3680 [22]
26415: 	media-type
26417: message/sipfrag
26420: Event
26421: A1,A2
26424: RFC 6665 [140]
26425: RFC 3515 [72]
26426: 	event-type
26428: refer
26431: Max-Forwards
26435: RFC 3261 [15]
26436: 	value
26438: 69
26441: Subscription-State
26445: RFC 6665 [140]
26446: 	substate-value
26448: active
26451: 	expires
26453: 300
26456: Content-Length
26460: RFC 3261 [15]
26461: RFC 3680 [22]
26462: 	value
26464: length of message-body
26468: Condition
26469: Explanation
26470: A1
26471: IMS security (A.6a/2 3GPP TS 34.229-2 [5])
26472: A2
26473: GIBA (A.6a/1 3GPP TS 34.229-2 [5])
26475: NOTE 1:	Branch parameter values sent by SS are different within a test case execution.
```

## A.2.12 MT REFER（行 26477-26664；used_by: TC-021）

关键官方标记：`REFER`、`Refer-To`、`Request-URI`、`CSeq`

```text
26477: A.2.12	MT REFER
26478: Header/param
26479: Cond
26480: Value/remark
26481: Rel
26482: Reference
26483: Request-Line
26487: RFC 3261 [15]
26488: 	Method
26490: REFER
26493: 	Request-URI
26495: same URI value as that which the UE has earlier sent in its Contact header within the dialog created by the INVITE sent by the UE when initiating the call to be transferred
26498: 	SIP-Version
26500: SIP/2.0
26503: Via
26505: order of the parameters in this header must be like in this table
26507: RFC 3261 [15]
26508: 	via-parm1:
26513: 		Sent-protocol
26515: SIP/2.0/UDP when using UDP or SIP/2.0/TCP when using TCP
26518: 		sent-by
26519: A1
26520: IP address and protected server port of SS
26523: 		sent-by
26524: A2
26525: IP address and unprotected server port of SS (optional)
26528: 		via-branch
26530: value starting with 'z9hG4bK'
26533: 	via-parm2:
26535: In addition to the via-parm entry for the SS, the following via-parm entries are included:
26538: 	via-parm
26540: SIP/2.0/UDP scscf1.3gpp.org;branch=z9hG4bK..., SIP/2.0/UDP scscf2.3gpp.org;branch=z9hG4bK..., SIP/2.0/UDP pcscf2.3gpp.org;branch=z9hG4bK...,
26541: SIP/2.0/UDP uas.3gpp.org:6543;branch=z9hG4bK...
26543: (NOTE 1)
26546: From
26550: RFC 3261 [15]
26551: 	addr-spec
26553: SIP URI of the SS which must be the same URI as used for the SS in the earlier requests within the dialog created by the INVITE sent by the UE when initiating the call to be transferred
26556: 	tag
26558: local tag of the dialog ID
26561: To
26565: RFC 3261 [15]
26566: 	addr-spec
26568: SIP URI of the UE which must be the same URI as used for UE in the earlier requests within the dialog created by the INVITE sent by the UE when initiating the call to be transferred
26571: 	tag	
26573: remote tag of the dialog ID
26576: Call-ID
26580: RFC 3261 [15]
26581: 	callid
26583: same value as in the first INVITE sent by the UE during setup of the call to be transferred
26586: CSeq
26590: RFC 3261 [15]
26591: 	value
26593: value of CSeq sent by the SS within its previous request in the dialog created by the INVITE sent by the UE when initiating the call to be transferred, but increased by one
26596: 	method
26598: REFER
26601: Contact
26605: RFC 3261 [15]
26606: 	addr-spec
26607: A1
26608: SIP URI with IP address or FQDN and protected server port of the SS (transferor)
26612: A2
26613: SIP URI with IP address or FQDN and unprotected server port of the SS (transferor)
26616: Refer-To
26620: RFC 3515 [72]
26621: 	addr-spec
26623: SIP or Tel URI of the transfer target
26626: Max-Forwards
26630: RFC 3261 [15]
26631: 	value
26633: non-zero value
26636: P-Access-Network-Info
26637: A1
26640: RFC 7315 [132]
26641: 	access-net-spec
26643: access network technology and, if applicable, the cell ID
26646: Content-Length
26650: RFC 3261 [15]
26651: 	value
26653: length of message-body
26657: Condition
26658: Explanation
26659: A1
26660: IMS security (A.6a/2 TS 34.229-2 [5])
26661: A2
26662: GIBA (A.6a/1 TS 34.229-2 [5])
26664: NOTE 1:	Branch parameter values sent by SS are different within a test case execution.
```

## A.3.1 200 OK for other requests than REGISTER or SUBSCRIBE（行 28196-28522；used_by: TC-012, TC-019, TC-020, TC-021）

关键官方标记：`200`、`OK`、`Contact`、`Content-Type`

```text
28196: A.3.1	200 OK for other requests than REGISTER or SUBSCRIBE
28197: Header/param
28198: Cond
28199: Value/remark
28200: Rel
28201: Reference
28202: Status-Line
28206: RFC 3261 [15]
28207: 	SIP-Version
28209: SIP/2.0
28212: 	Status-Code
28214: 200
28217: 	Reason-Phrase
28219: OK
28222: Via
28224: not present
28226: RFC 3261 [15]
28227: 	via-parm
28229: same value as received in request
28232: Record-Route
28234: order of the parameters in this header must be like in the respective rows
28236: RFC 3261 [15]
28237: 	rec-route
28238: A1
28239: <sip:pcscf.other.com;lr>, <sip:scscf.other.com;lr>, <sip:orig@scscf.3gpp.org;lr>, <sip:SS P-CSCF address: protected server port of SS;lr>
28243: A3
28244: <sip:pcscf.other.com;lr>, <sip:scscf.other.com;lr>, <sip:orig@scscf.3gpp.org;lr>, <sip:SS P-CSCF address: unprotected server port of SS (optional);lr>
28248: A2,A4,
28249: A5
28250: same value as received in the request (if present in the request)
28251: Note: for requests other than INVITE it is not regulated if and what the UE writes into this header in a response.
28255: A6
28256: <sip:orig@ecscf.other.com;lr>, <sip:SS P-CSCF address:protected server port of SS;lr>
28260: A7
28261: <sip:orig@ecscf.other.com;lr>, <sip:SS P-CSCF address:unprotected server port of SS;lr>
28264: From
28268: RFC 3261 [15]
28269: 	addr-spec
28271: same value as received in request
28274: 	tag
28276: same value as received in request
28279: To
28283: RFC 3261 [15]
28284: 	addr-spec
28286: same value as received in request
28289: 	tag
28291: same value as received in request or any value added if missing from request
28294: P-Asserted-Identity
28298: RFC 3325 [89]
28299: 	addr-spec
28301: A tel URI that can be recognized as valid emergency numbers if dialled by the user are specified in 3GPP TS 22.101 [39]. 
28302: The emergency numbers 112 and 911 are stored on the ME, in accordance with 3GPP TS 22.101 [39]
28305: 	uri-parameter
28307: lr
28310: Contact
28311: A1,A2
28312: A3,A4
28315: RFC 3261 [15]
28316: RFC 5627 [61
28317: 	addr-spec 
28318: A1,A3
28319: px_IMS_CalleeContactUri
28323: A2 AND NOT A9
28324: SIP URI with IP address or FQDN and protected server port of UE
28328: A4 AND NOT A9
28329: SIP URI with IP address or FQDN and unprotected server port of UE
28333: A2 AND A9
28334: Public GRUU as obtained during registration as pub-gruu contact parameter of the 200 OK for REGISTER response
28338: A4 AND A9
28339: Public GRUU as obtained during registration as pub-gruu contact parameter of the 200 OK for REGISTER response
28342: 	feature-param
28343: A10
28344: audio
28348: A18 AND (A19 OR A20)
28349: video
28351: IR.94 [134]
28353: A11 AND A14 AND (A15 OR A16)
28354: audio
28357: Call-ID
28361: RFC 3261 [15]
28362: 	callid
28364: same value as received in request
28367: Call-Info
28371: RFC 8147 [149]
28372: 	cid URL
28374: psap@3gpp.org
28375: Rel-14
28377: 	purpose
28379: EmergencyCallData.Control
28382: CSeq
28386: RFC 3261 [15]
28387: 	value
28389: same value as received in request
28392: P-Access-Network-Info
28393: A8
28397: 	access-net-spec
28399: access network technology and, if applicable, the cell ID
28402: Accept
28406: RFC 8147 [149]
28407: 	media-range
28409: application/sdp, application/pidf+xml, application/EmergencyCallData.Control+xml, application/emergencyCallData.eCall.MSD
28410: Rel-14
28412: Recv-Info
28416: RFC 8147 [149]
28417: 	Info-package-type
28418: A12
28419: emergencyCallData.eCall.MSD
28420: Rel-14
28422: Content-Type
28426: RFC 8147 [149]
28427: 	media-type
28428: A12
28429: multipart/mixed; boundary=boundary1
28430: Rel-14
28432: Content-Length
28433: A10
28436: RFC 3261 [15]
28437: 	value
28438: NOT A12
28439: 0
28443: A12
28444: length of message body
28447: Message-body
28453: A13
28454: --boundary1
28455: Content-Type: application/EmergencyCallData.eCall.Control+xml
28456: Content-ID: same cid as in Call-Info header
28457: Content-Disposition: by-reference
28458: <?xml version="1.0" encoding="UTF-8"?>
28459: <EmergencyCallData.control
28460: xmlns="urn:ietf:params:xml:ns:EmergencyCallData:control">
28461: <ack received="true" ref=" cid URL of MIME body part containing the MSD sent by the UE in INVITE"/>
28462: </EmergencyCallData.control>
28463: --boundary1
28465: RFC 8147 [149]
28467: A14
28468: --boundary1
28469: Content-Type: application/EmergencyCallData.eCall.Control+xml
28470: Content-Disposition: by-reference
28471: <?xml version="1.0" encoding="UTF-8"?>
28472: <emergencyCallData.Control
28473: xmlns="urn:ietf:params:xml:ns:EmergencyCallData:control">
28474: <ack received="false" ref=" cid URL of MIME body part containing the MSD sent by the UE in INVITE "/>
28475: </EmergencyCallData.control>
28476: --boundary1
28478: RFC 8147 [149]
28480: Condition
28481: Explanation
28482: A1
28483: Response sent by SS for INVITE/UPDATE (IMS security, A.6a/2 TS 34.229-2 [5]))
28484: A2
28485: Response sent by UE for INVITE/UPDATE (IMS security, A.6a/2 TS 34.229-2 [5]))
28486: A3
28487: Response sent by SS for INVITE/UPDATE (GIBA, A.6a/1 TS 34.229-2 [5]))
28488: A4
28489: Response sent by UE for INVITE/UPDATE (GIBA, A.6a/1 TS 34.229-2 [5]))
28490: A5
28491: Any response sent by the UE within a dialog
28492: A6
28493: Response sent by SS for INVITE for emergency call or non-UE detectable emergency call
28494: A7
28495: Response sent by SS for INVITE for emergency call without emergency registration
28496: A8
28497: Any response sent by the UE within a dialog, except for CANCEL requests
28498: A9
28499: obtaining and using GRUUs in the Session Initiation Protocol (SIP) (A.4/53 3GPP TS 34.229-2 [5])
28500: A10
28501: Response sent by SS
28502: A11
28503: Response sent by UE
28504: A12
28505: Response sent by SS for INVITE for eCall over IMS session with either ACK or NACK
28506: A13
28507: Response sent by SS for INVITE for eCall over IMS session with ACK element = TRUE
28508: A14
28509: Response sent by SS for INVITE for eCall over IMS session with ACK element = FALSE
28510: A15
28511: UE supports audio media feature tag (A.12/56 3GPP TS 34.229-2 [5])
28512: A16
28513: UE uses E-UTRAN access and has received IMS voice over PS Session Supported Indication in the NAS ATTACH ACCEPT message as described in TS 24.301 [150], clauses 8.2.1 and 9.9.3.12A
28514: A17
28515: UE uses UTRAN/GERAN access and has received IMS voice over PS Session Supported Indication in the NAS ATTACH ACCEPT message as described in TS 24.008 [12], clauses 9.4.2 and 10.5.5.23
28516: A18
28517: UE supports video feature tag (A.12/32 3GPP TS 34.229-2 [5])
28518: A19
28519: Response sent by SS for INVITE
28520: A20
28521: Response sent by UE for INVITE
```

## A.3.3 202 Accepted（行 28644-28721；used_by: TC-021）

关键官方标记：`202`、`Accepted`

```text
28644: A.3.3	202 Accepted
28645: Header/param
28646: Value/remark
28647: Rel
28648: Reference
28649: Status-Line
28652: RFC 3261 [15]
28653: 	SIP-Version
28654: SIP/2.0
28657: 	Status-Code
28658: 202
28661: 	Reason-Phrase
28662: Accepted
28665: Via
28668: RFC 3261 [15]
28669: 	via-parm
28670: same value as received in request
28673: From
28676: RFC 3261 [15]
28677: 	addr-spec
28678: same value as received in request
28681: 	tag
28682: same value as received in request
28685: To
28688: RFC 3261 [15]
28689: 	addr-spec
28690: same value as received in request
28693: 	tag
28694: same value as received in request or common to-tag (message) added if missing from request
28697: Call-ID
28700: RFC 3261 [15]
28701: 	callid
28702: same value as received in request
28705: CSeq
28708: RFC 3261 [15]
28709: 	value
28710: same value as received in request
28713: Content-Length
28714: optional when sent by the UE
28716: RFC 3261 [15]
28717: 	value
28718: 0
```

## A.5.3 NOTIFY for conference event package（行 29854-30102；used_by: TC-021）

关键官方标记：`NOTIFY`、`Event`、`conference`、`Subscription-State`

```text
29854: A.5.3	NOTIFY for conference event package
29855: Header/param
29856: Cond
29857: Value/remark
29858: Rel
29859: Reference
29860: Request-Line
29864: RFC 3261 [15]
29865: 	Method
29867: NOTIFY
29870: 	Request-URI
29872: UE's contact address in SIP URI form, as provided in the Contact header within the SUBSCRIBE creating the dialog
29875: 	SIP-Version
29877: SIP/2.0
29880: Via
29882: order of the parameters in this header must be like in this table
29884: RFC 3261 [15]
29885: 	via-parm1:
29890: 		Sent-protocol
29892: SIP/2.0/UDP when using UDP or SIP/2.0/TCP when using TCP
29895: 		sent-by
29896: A1
29897: IP address and protected server port of SS
29900: 		sent-by
29901: A2
29902: IP address and unprotected server port of SS (optional)
29905: 		via-branch
29907: value starting with 'z9hG4bK' (NOTE 2)
29910: 	via-parm2:
29915: 		sent-protocol
29917: SIP/2.0/UDP when using UDP or SIP/2.0/TCP when using TCP
29920: 		sent-by
29922: scscf.3gpp.org
29925: 		via-branch	
29927: value starting with 'z9hG4bK' (NOTE 2)
29930: From
29934: RFC 3261 [15]
29935: 	addr-spec
29937: sip:final@conf-factory. appended with px_IMS_HomeDomainName
29940: 	tag
29942: tag value corresponding to the SIP URI in the From header
29945: To
29949: RFC 3261 [15]
29950: 	addr-spec
29952: any IMPU within the set of IMPUs on ISIM
29955: 	tag	
29957: tag value corresponding to the SIP URI in the To header
29960: Call-ID
29964: RFC 3261 [15]
29965: 	callid
29967: same as value received in SUBSCRIBE message
29970: CSeq
29974: RFC 3261 [15]
29975: 	value
29977: value of CSeq sent by the SS within its previous request in the same dialog but increased by one
29980: 	method
29982: NOTIFY
29985: Contact
29989: RFC 3261 [15]
29990: 	addr-spec
29992: sip:final@conf-factory. appended with px_IMS_HomeDomainName
29995: Content-Type
29996: A3
29999: RFC 3261 [15]
30000: RFC 4575 [86]
30001: 	media-type
30003: application/conference-info+xml
30006: Event
30010: RFC 6665 [140]
30011: RFC 4575 [86]
30012: 	event-type
30014: conference
30017: Max-Forwards
30021: RFC 3261 [15]
30022: 	value
30024: 69
30027: Subscription-State
30031: RFC 6665 [140]
30032: 	substate-value
30033: A3
30034: active
30037: 	expires
30038: A3
30039: 7200
30042: 	substate-value
30043: A4
30044: terminated
30046: RFC 4575 [86]
30047: 	reason
30048: A4
30049: noresource
30051: RFC 6665 [140]
30052: Content-Length
30056: RFC 3261 [15]
30059: RFC 4575 [86]
30060: 	value
30062: length of message-body
30065: Message-body
30066: A3
30067:  <?xml version="1.0" encoding="UTF-8"?>
30068:  <conference-info   xmlns="urn:ietf:params:xml:ns:conference-info">
30069:                       entity="sip:final@conf-factory. appended with px_IMS_HomeDomainName" 
30070:                       state="full" 
30071:                       version="0" 
30072:    <users>
30073:      <user entity=" any IMPU within the set of IMPUs on ISIM">
30074:       <endpoint entity=" Contact URI of the UE">
30075:        <status>connected</status>
30076:        <joining-method>dialed-in</joining-method>
30077:        <media id="1">
30078:         <type>audio</type>
30079:         <label>34567</label>
30080:         <src-id>SSRC of UE's RTP packets</src-id>
30081:         <status>sendrecv</status>
30082:        </media>
30083:       </endpoint>
30084:      </users>
30085:    </conference-info>
30089: Condition
30090: Explanation
30091: A1
30092: IMS security (A.6a/2 TS 34.229-2 [5]))
30093: A2
30094: GIBA (A.6a/1 TS 34.229-2 [5]))
30095: A3
30096: SS sends NOTIFY to indicate that UE is now subscribed to the conference event package
30097: A4
30098: SS sends NOTIFY to indicate that UE's subscription to conference event is terminated now
30100: NOTE1:	All choices for applicable conditions are described for each header.
30101: NOTE 2:	Branch parameter values sent by SS are different within a test case execution.
```

> 状态：官方 Annex A 默认消息内容已锚定，作为呼叫类用例的 `.3.3` 等价骨架；正式一致性判定仍需 SS/一致性仪表按 34.229-1 对应子节对表执行。

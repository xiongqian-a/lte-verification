# TC-011 / TC-014 Annex A 默认消息内容（官方 .3.3 等价）

来源：`3GPP TS 34.229-1` V14.7.0 (2019-06) Annex A，逐行抽取自 `<standards-extract>\34229-1e70-word.txt`；行号口径 `Python str.splitlines()`（与 `34229-1e70_ascii.txt` 交叉校验一致）。

说明：34.229-1 Annex C.2 明确 `The default message contents in annex A are used`，TC-011（8.1）与 TC-014（8.2）都执行 C.2，因此这些 Annex A 消息表就是两个用例的 `.3.3 Specific message contents` 等价物。

## A.1.1 REGISTER（行 21415-22020；used_by: TC-011, TC-014）

关键官方标记：`Initial unprotected REGISTER`、`Subsequent REGISTER sent over security associations`、`UE initiated IMS re-registration or de-registration`、`Security-Client`、`Security-Verify`、`Authorization`、`Expires`、`P-Access-Network-Info`、`AKAv1-MD5`

```text
21415: A.1.1	REGISTER
21416: Header/param
21417: Cond
21418: Value/remark
21419: Rel
21420: Reference
21421: Request-Line
21425: RFC 3261 [15]
21426: 	Method
21428: REGISTER
21431: 	Request-URI
21433: SIP URI formed from home domain name as stored in EFDOMAIN (when using ISIM) or
21434: SIP URI formed from home domain name derived from the IMSI (when no ISIM available on the UICC)
21437: 	Request-URI
21438: A14,A15
21439: SIP URI formed from home domain name as preconfigured in the UE
21442: 	SIP-Version
21444: SIP/2.0
21447: Route
21449: not present
21451: RFC 3261 [15]
21452: Via
21456: RFC 3261 [15]
21457: 	sent-protocol
21459: SIP/2.0/UDP (when using UDP) or 
21460: SIP/2.0/TCP (when using TCP)
21463: 	sent-by
21464: A1,A3,
21465: A14,A15
21466: IP address or FQDN, port (optional) and not checked
21470: A2
21471: IP address or FQDN and, when using UDP, protected server port of the UE
21474: 	response-port
21475: A1,A3
21476: rport (when using UDP)
21478: RFC 3581 [96]
21479: 	via-branch
21481: value starting with 'z9hG4bK'
21484: From
21488: RFC 3261 [15]
21489: 	addr-spec
21490: A1
21491: any IMPU within the set of IMPUs on ISIM (when using ISIM; NOTE 3) or
21492: public user identity derived from IMSI (when no ISIM available on the UICC)
21496: A2,A15
21497: same public user identity as in initial REGISTER
21501: A3 AND NOT A7
21502: public user identity derived from IMSI
21506: A7
21507: emergency public user identity (NOTE 4)
21511: A14
21512: IMPU preconfigured in the UE
21516: A17
21517: same public user identity as in initial REGISTER
21520: 	tag
21522: must be present, value not checked
21525: To
21529: RFC 3261 [15]
21530: 	addr-spec
21531: A1
21532: any IMPU within the set of IMPUs on ISIM (when using ISIM; NOTE 3) or
21533: public user identity derived from IMSI (when no ISIM available on the UICC)
21537: A2,A15
21538: same public user identity as in initial REGISTER
21542: A3 AND NOT A7
21543: public user identity derived from IMSI
21547: A7
21548: emergency public user identity (NOTE 4)
21552: A14
21553: IMPU preconfigured in the UE
21557: A17
21558: same public user identity as in initial REGISTER
21561: 	tag
21563: not present
21566: Contact
21570: RFC 3261 [15]
21571: 	addr-spec
21572: A1,A3,
21573: A14,A15
21574: SIP URI with IP address or FQDN and indicating either an unprotected port selected by the UE or no port at all
21578: A2
21579: SIP URI with IP address or FQDN and protected server port of UE
21583: A7
21584: The SIP URI shall contain the sos URI parameter
21587: 	feature-param
21588: A4
21589: +g.3gpp.icsi-ref="(comma-separated list of tag-values)" with comma-separated list of tag-values containing at least tag-value urn%3Aurn-7%3A3gpp-service.ims.icsi.mmtel" (see NOTE 2,5)
21593: A6 AND NOT A7
21594: +g.3gpp.smsip
21598: A10
21599: video
21603: A28 AND (A29 OR A30)
21604: audio
21608: A11 AND NOT A7
21609: +g.3gpp.cs2ps-srvcc
21610: Rel-11
21613: A12 AND NOT A7
21614: +g.3gpp.cs2ps-srvcc-alerting
21615: Rel-11
21618: A13 AND NOT A16
21619: +g.3gpp.accesstype="cellular2"
21620: Rel-11
21621: RFC 3840 [63]
21623: A13 AND A16
21624: +g.3gpp.accesstype="wlan1"
21625: Rel-11
21626: RFC 3840 [63]
21627: 	c-p-instance
21628: A5
21629: +sip.instance="<urn:gsma:imei: (gsma-specifier-defined-substring)>"
21630: where gsma-specifier-defined-substring shall be the IMEI code of the UE, coded as specified in RFC 7254 [122], without optional parameters
21631: Rel-10
21632: RFC 5627 [61]
21633: RFC 7254 [122]
21634: 	expires
21636: 600000 (if present)
21639: Expires
21641: present if no expires parameter in Contact header
21643: RFC 3261 [15]
21644: 	delta-seconds
21646: 600000
21649: Require
21650: A1,A2
21653: RFC 3261 [15]
21654: RFC 3329 [21]
21655: 	option-tag
21657: sec-agree
21660: Proxy-Require
21661: A1,A2
21664: RFC 3261 [15]
21665: RFC 3329 [21]
21666: 	option-tag
21668: sec-agree
21671: Supported
21675: RFC 3261 [15]
21676: TS 24.229 [10]
21677: 	option-tag
21678: A5
21679: gruu
21684: path
21687: CSeq
21691: RFC 3261 [15]
21692: 	value
21693: A1,A3
21694: A14
21695: must be present, value not checked
21699: A2,A15
21700: must be incremented from the previous REGISTER
21703: 	method
21705: REGISTER
21708: Call-ID
21712: RFC 3261 [15]
21713: 	callid
21715: value not checked
21718: Security-Client
21719: A1,A2
21722: RFC 3329 [21]
21723: RFC 4835 [124]
21724: 	mechanism-name
21726: ipsec-3gpp
21729: 	algorithm
21731: hmac-sha-1-96
21734: 	protocol
21736: esp (if present)
21739: 	mode
21741: trans (if present)
21744: 	encrypt-algorithm
21746: des-ede3-cbc or aes-cbc or null
21749: 	spi-c
21751: SPI number of the inbound SA at the protected client port
21754: 	spi-s
21756: SPI number of the inbound SA at the protected server port
21759: 	port-c
21761: protected client port
21764: 	port-s
21766: protected server port
21769: Security-Client
21770: A14,A15
21771: not present
21774: Security-Verify
21775: A2
21778: RFC 3329 [21]
21779: 	sec-mechanism
21780: A2
21781: same value as Security-Server header sent by SS
21784: Security-Verify
21785: A1,A3
21786: A14,A15
21787: not present
21790: Authorization
21791: A1
21792: Digest
21794: RFC 2617 [16]
21795: RFC 3310 [17]
21796: 	username
21797: A1
21798: private user identity as stored in EFIMPI (when using ISIM) or
21799: private user identity derived from IMSI (when no ISIM available on the UICC)
21802: 	realm
21803: A1
21804: home domain name as stored in EFDOMAIN (when using ISIM) or
21805: home domain name derived from the IMSI (when no ISIM available on the UICC)
21808: 	nonce
21809: A1
21810: set to an empty value
21813: 	digest-uri
21814: A1
21815: SIP URI formed from home domain name as stored in EFDOMAIN (when using ISIM) or formed from home domain name derived from the IMSI (when no ISIM available on the UICC)
21818: 	response
21819: A1
21820: set to an empty value
21823: Authorization
21824: A14(o)
21825: Header optional
21828: 	username
21829: A14
21830: user identity as preconfigured in the UE
21833: 	realm
21834: A14
21835: home domain name as preconfigured in the UE
21838: 	nonce
21839: A14
21840: set to an empty value
21843: 	digest-uri
21844: A14
21845: preconfigured in the UE
21848: 	response
21849: A14
21850: set to an empty value
21853: Authorization
21854: A2,A15
21855: Digest
21857: RFC 2617 [16]
21858: RFC 3310 [17]
21859: 	username
21860: A2
21861: private user identity as stored in EFIMPI (when using ISIM) or
21862: private user identity derived from IMSI (when no ISIM available on the UICC)
21866: A15
21867: user identity as preconfigured in the UE
21870: 	realm
21871: A2,A15
21872: same value as received in the realm directive in the WWW Authenticate header sent by SS
21875: 	nonce
21876: A2,A15
21877: same value as in WWW-Authenticate header sent by SS
21880: 	opaque
21881: A2,A15
21882: same value as sent by the server in "401 Unauthorized for REGISTER"
21885: 	digest-uri
21886: A2
21887: SIP URI formed from home domain name as stored in EFDOMAIN (when using ISIM) or formed from home domain name derived from the IMSI (when no ISIM available on the UICC)
21891: A15
21892: SIP URI formed from home domain name as preconfigured in the UE
21895: 	qop-value
21896: A2,A15
21897: auth
21900: 	cnonce-value
21901: A2,A15
21902: value assigned by UE affecting the response calculation
21905: 	nonce-count
21906: A2,A15
21907: counter to indicate how many times UE has sent the same value of nonce within successive REGISTER requests, initial value shall be 1
21910: 	response
21911: A2
21912: response calculated by UE
21916: A15
21917: response calculated by UE using password px_DigestPasswordForSIP
21920: 	algorithm
21921: A2
21922: AKAv1-MD5
21926: A15
21927: MD5
21930: Max-Forwards
21934: RFC 3261 [15]
21935: 	value
21937: non-zero value
21940: P-Access-Network-Info
21941: A2,A15,
21942: A14(o),
21943: A16(o)
21946: RFC 7315 [132]
21947: 	access-net-spec
21948: A2
21949: access network technology and, if applicable, the cell ID
21953: A14,A15
21954: access network technology for Fixed Broadband with access-type field matching "*DLS*" and a "dsl-location" parameter (value not checked)
21958: A16
21959: access network technology, containing any of "IEEE-802.11", "IEEE-802.11a", "IEEE-802.11b", "IEEE-802.11g" or "IEEE-802-11n", and i-wlan-node-id parameter containing a MAC address according to TS 24.229 [10], 7.2A.4.2. Value of MAC address not to be checked
21962: Content-Length
21964: header shall be present if UE uses TCP to send this message and if there is a message-body
21966: RFC 3261 [15]
21967: 	value
21969: length of request body, if such is present
21973: Condition
21974: Explanation
21975: A1
21976: Initial unprotected REGISTER (IMS security, A.6a/2 3GPP TS 34.229-2 [5])
21977: A2
21978: Subsequent REGISTER sent over security associations (IMS security, A.6a/2 3GPP TS 34.229-2 [5]) 
21979: A3
21980: REGISTER for the case UE supports GIBA (A.6a/1 3GPP TS 34.229-2 [5])
21981: A4
21982: UE supports IMS Multimedia Telephony (MTSI) (A.3A/50 3GPP TS 34.229-2 [5])
21983: A5
21984: obtaining and using GRUUs in the Session Initiation Protocol (SIP) (A.4/53 3GPP TS 34.229-2 [5]). Mandatory from Rel-10 onwards.
21985: A6
21986: UE supports SM-over-IP receiver (A.3A/62 3GPP TS 34.229-2 [5])
21987: A7
21988: Initial unprotected or subsequent REGISTER for emergency registration
21989: A8
21990: Void
21991: A10
21992: UE supports video feature tag (A.12/32 3GPP TS 34.229-2 [5])
21993: A11
21994: UE supports CS to PS SRVCC (A.12/40 3GPP TS 34.229-2 [5])
21995: A12
21996: UE supports CS to PS SRVCC in alerting state (A.12/41 3GPP TS 34.229-2 [5])
21997: A13
21998: UE indicates g.3gpp.accesstype media feature tag in REGISTER (A.12/46 3GPP TS 34.229-2 [5])
21999: A14
22000: Initial REGISTER SIP Digest without TLS for Fixed Broadband Access (SIP Digest without TLS, A.6a/5 3GPP TS 34.229-2 [5])
22001: A15
22002: Subsequent REGISTER SIP Digest without TLS for Fixed Broadband Access (SIP Digest without TLS, A.6a/5 3GPP TS 34.229-2 [5])
22003: A16
22004: IMS registration over WLAN
22005: A17
22006: UE initiated IMS re-registration or de-registration (A.12/51 3GPP TS 34.229-2 [5])
22007: A18-A27
22008: Void
22009: A28
22010: UE supports audio media feature tag (A.12/56 3GPP TS 34.229-2 [5])
22011: A29
22012: UE uses E-UTRAN access and has received IMS voice over PS Session Supported Indication in the NAS ATTACH ACCEPT message as described in TS 24.301 [150], clauses 8.2.1 and 9.9.3.12A
22013: A30
22014: UE uses UTRAN/GERAN access and has received IMS voice over PS Session Supported Indication in the NAS ATTACH ACCEPT message as described in TS 24.008 [12], clauses 9.4.2 and 10.5.5.23
22016: NOTE 1:	All choices for applicable conditions are described for each header.
22017: NOTE 2:	The "=" may include optional linear white spaces according to the EQUAL definition in chapter 25.1, RFC 3261 [15].
22018: NOTE 3:	Public user identity shall be the same for 'From' and 'To'.
22019: NOTE 4:	According to TS 24.229 clause 5.1.1.1A and 5.1.6.2 [10] when the UE is using ISIM the emergency public user identity is the first public user identity in the list stored in the ISIM; when there is no ISIM it is the default public user id if the UE successfully performed IMS registration with the IM CN subsystem before, and the temporary user id (derived from IMSI) in all other cases.
22020: NOTE 5:	URN is the outcome of the  URL encoding ("Percent-Encoding" according to RFC 3986 [129]) of urn:urn-7:3gpp-service.ims.icsi.mmtel.
```

### A.1.1 condition 词表（行 21973-22014）

```text
21973: Condition
21974: Explanation
21975: A1
21976: Initial unprotected REGISTER (IMS security, A.6a/2 3GPP TS 34.229-2 [5])
21977: A2
21978: Subsequent REGISTER sent over security associations (IMS security, A.6a/2 3GPP TS 34.229-2 [5]) 
21979: A3
21980: REGISTER for the case UE supports GIBA (A.6a/1 3GPP TS 34.229-2 [5])
21981: A4
21982: UE supports IMS Multimedia Telephony (MTSI) (A.3A/50 3GPP TS 34.229-2 [5])
21983: A5
21984: obtaining and using GRUUs in the Session Initiation Protocol (SIP) (A.4/53 3GPP TS 34.229-2 [5]). Mandatory from Rel-10 onwards.
21985: A6
21986: UE supports SM-over-IP receiver (A.3A/62 3GPP TS 34.229-2 [5])
21987: A7
21988: Initial unprotected or subsequent REGISTER for emergency registration
21989: A8
21990: Void
21991: A10
21992: UE supports video feature tag (A.12/32 3GPP TS 34.229-2 [5])
21993: A11
21994: UE supports CS to PS SRVCC (A.12/40 3GPP TS 34.229-2 [5])
21995: A12
21996: UE supports CS to PS SRVCC in alerting state (A.12/41 3GPP TS 34.229-2 [5])
21997: A13
21998: UE indicates g.3gpp.accesstype media feature tag in REGISTER (A.12/46 3GPP TS 34.229-2 [5])
21999: A14
22000: Initial REGISTER SIP Digest without TLS for Fixed Broadband Access (SIP Digest without TLS, A.6a/5 3GPP TS 34.229-2 [5])
22001: A15
22002: Subsequent REGISTER SIP Digest without TLS for Fixed Broadband Access (SIP Digest without TLS, A.6a/5 3GPP TS 34.229-2 [5])
22003: A16
22004: IMS registration over WLAN
22005: A17
22006: UE initiated IMS re-registration or de-registration (A.12/51 3GPP TS 34.229-2 [5])
22007: A18-A27
22008: Void
22009: A28
22010: UE supports audio media feature tag (A.12/56 3GPP TS 34.229-2 [5])
22011: A29
22012: UE uses E-UTRAN access and has received IMS voice over PS Session Supported Indication in the NAS ATTACH ACCEPT message as described in TS 24.301 [150], clauses 8.2.1 and 9.9.3.12A
22013: A30
22014: UE uses UTRAN/GERAN access and has received IMS voice over PS Session Supported Indication in the NAS ATTACH ACCEPT message as described in TS 24.008 [12], clauses 9.4.2 and 10.5.5.23
```

### A.1.1 脚注（行 22016-22020）

```text
22016: NOTE 1:	All choices for applicable conditions are described for each header.
22017: NOTE 2:	The "=" may include optional linear white spaces according to the EQUAL definition in chapter 25.1, RFC 3261 [15].
22018: NOTE 3:	Public user identity shall be the same for 'From' and 'To'.
22019: NOTE 4:	According to TS 24.229 clause 5.1.1.1A and 5.1.6.2 [10] when the UE is using ISIM the emergency public user identity is the first public user identity in the list stored in the ISIM; when there is no ISIM it is the default public user id if the UE successfully performed IMS registration with the IM CN subsystem before, and the temporary user id (derived from IMSI) in all other cases.
22020: NOTE 5:	URN is the outcome of the  URL encoding ("Percent-Encoding" according to RFC 3986 [129]) of urn:urn-7:3gpp-service.ims.icsi.mmtel.
```

## A.1.2 401 Unauthorized for REGISTER（行 22021-22255；used_by: TC-011, TC-014）

关键官方标记：`SIP/2.0`、`401`、`Unauthorized`、`WWW-Authenticate`、`Security-Server`、`AKAv1-MD5`

```text
22021: A.1.2	401 Unauthorized for REGISTER
22022: Header/param
22023: Cond
22024: Value/remark
22025: Rel
22026: Reference
22027: Status-Line
22031: RFC 3261 [15]
22032: 	SIP-Version
22034: SIP/2.0
22037: 	Status-Code
22039: 401
22042: 	Reason-Phrase
22044: Unauthorized
22047: Via
22051: RFC 3261 [15]
22052: 	via-parm
22054: same value as received in REGISTER message
22057: To
22061: RFC 3261 [15]
22062: 	addr-spec
22064: same value as received in REGISTER message
22067: 	tag
22069:  common to-tag (register)
22072: From
22076: RFC 3261 [15]
22077: 	addr-spec
22079: same value as received in REGISTER message
22082: 	tag
22084: same value as received in REGISTER message
22087: Call-ID
22091: RFC 3261 [15]
22092: 	callid
22094: same value as received in REGISTER message
22097: CSeq
22101: RFC 3261 [15]
22102: 	value
22104: same value as received in REGISTER message
22107: WWW-Authenticate
22111: RFC 2617 [16]
22112: RFC 3310 [17]
22113: 	realm
22115: home domain name as stored in EFDOMAIN or home domain name derived from the IMSI
22118: 	realm
22119: A2
22120: home domain name as preconfigured in the UE
22123: 	algorithm
22124: A1
22125: AKAv1-MD5
22128: 	algorithm
22129: A2
22130: MD5
22133: 	qop-value
22135: auth
22138: 	nonce
22140: Base 64 encoding of RAND and AUTN
22143: 	opaque
22145: arbitrary value (to be returned by the UE in subsequent REGISTER)
22148: Security-Server
22149: A1
22152: RFC 3329 [21]
22153: 	mechanism-name
22155: ipsec-3gpp
22158: 	algorithm
22160: px_IMS_SecAlgorithm (hmac-md5-96 or hmac-sha-1-96)
22163: 	spi-c
22165: SPI number of the inbound SA at the protected client port
22168: 	spi-s
22170: SPI number of the inbound SA at the protected server port
22173: 	port-c
22175: protected client port of SS
22178: 	port-s
22180: protected server port of SS
22183: 	Encrypt-algorithm
22185: des-ede3-cbc or aes-cbc
22188: 	q
22190: 0.9
22193: 	Mechanism-name 
22195: Ipsec-3gpp
22198: 	algorithm
22200: Algorithm not selected by px_IMS_IPSecAlgorithm (hmac-sha-1-96 or hmac-md5-96)
22203: 	spi-c
22205: SPI number of the inbound SA at the protected client port
22208: 	spi-s
22210: SPI number of the inbound SA at the protected server port
22213: 	port-c
22215: protected client port of SS
22218: 	port-s
22220: protected server port of SS
22223: 	encrypt-algorithm
22225: des-ede3-cbc or aes-cbc
22228: 	q
22230: 0.7
22233: Security-Server
22234: A2
22235: not present
22238: Content-Length
22242: RFC 3261 [15]
22243: 	value
22245: 0
22249: Condition
22250: Explanation
22251: A1
22252: IMS Security (A.6a/2 3GPP TS 34.229-2 [5])
22253: A2
22254: SIP Digest without TLS for Fixed Broadband Access (SIP Digest without TLS, A.6a/5 3GPP TS 34.229-2 [5])
```

## A.1.3 200 OK for REGISTER（行 22256-22497；used_by: TC-011, TC-014）

关键官方标记：`200`、`OK`、`Contact`、`P-Associated-URI`、`Service-Route`

```text
22256: A.1.3	200 OK for REGISTER
22257: Header/param
22258: Cond
22259: Value/remark
22260: Rel
22261: Reference
22262: Status-Line
22266: RFC 3261 [15]
22267: 	SIP-Version
22269: SIP/2.0
22272: 	Status-Code
22274: 200
22277: 	Reason-Phrase
22279: OK
22282: Via
22286: RFC 3261 [15]
22287: 	via-parm
22289: same value as received in REGISTER message
22292: To
22296: RFC 3261 [15]
22297: 	addr-spec
22299: same value as received in REGISTER message
22302: 	tag
22304: common to-tag (register)
22307: From
22311: RFC 3261 [15]
22312: 	addr-spec
22314: same value as received in REGISTER message
22317: 	tag
22319: same value as received in REGISTER message
22322: Call-ID
22326: RFC 3261 [15]
22327: 	callid
22329: same value as received in REGISTER message
22332: CSeq
22336: RFC 3261 [15]
22337: 	value
22339: same value as received in REGISTER message
22342: Contact
22346: RFC 3261 [15]
22347: RFC 5627 [61]
22348: 	addr-spec
22350: same value as received in REGISTER message
22353: 	pub-gruu
22354: A1
22355: Public GRUU as the SIP URI got from the To header of the REGISTER request, together with the gr parameter with an arbitrary value
22358: 	temp-gruu
22359: A1
22360: Temporary GRUU with an arbitrary value in the user part and the host part matching with the domain of the To header of the REGISTER and gr parameter without any value
22363: 	temp-gruu
22364: A3
22365: not present
22368: 	feature-param
22370: same value as received in REGISTER message
22373: 	expires
22375: 600000
22378: P-Associated-URI
22380: order of the parameters in this header must be like in this table 
22382: RFC 7315 [132]
22383: 	addr-spec
22384: A2
22385: all the IMPUs within the set of IMPUs on ISIM (NOTE 1)
22388: 	addr-spec
22389: A2
22390: additional associated TEL URI (NOTE2)
22398: P-Associated-URI
22399: 	addr-spec
22400: A3
22403: emergency public user identity (NOTE 3)
22405: RFC 7315 [132]
22406: P-Associated-URI
22407: A5
22408: order of the parameters in this header must be like in this table 
22410: RFC 7315 [132]
22411: 	addr-spec
22413: IMPU preconfigured in the UE
22416: 	addr-spec
22418: additional associated TEL URI (NOTE2)
22421: Service-Route
22422: A2
22425: RFC 3608 [19]
22426: 	addr-spec
22428: scscf.3gpp.org
22431: 	uri-parameter
22433: lr
22436: Path
22440: RFC 3327 [20]
22441: 	addr-spec
22443: SS P-CSCF address
22446: 	uri-parameter
22448: lr
22451: Feature-Caps
22455: RFC 6809 [125]
22456:     feature-param
22457: A4
22458: +g.3gpp.atcf="tel:+1-237-888-9999"
22459: Rel-11
22461:     feature-param
22462: A4
22463: +g.3gpp.cs2ps-srvcc="<sip:sti-sr@atcf.visited2.net>" 
22464: Rel-11
22466: Feature-Caps
22467: A5
22468: not present
22471: Content-Length
22475: RFC 3261 [15]
22476: 	value
22478: 0
22482: Condition
22483: Explanation
22484: A1
22485: obtaining and using GRUUs in the Session Initiation Protocol (SIP) (A.4/53 3GPP TS 34.229-2 [5])
22486: A2
22487: Response for an non-emergency registration
22488: A3
22489: Response for an emergency registration
22490: A4
22491: Response if the UE provided the +g.3gpp.cs2ps-srvcc and +g.3gpp.cs2ps-srvcc-alerting feature-params in the REGISTER message
22492: A5
22493: SIP Digest without TLS for Fixed Broadband Access (SIP Digest without TLS, A.6a/5 3GPP TS 34.229-2 [5])
22495: NOTE 1:	The set of IMPUs shall be in accordance to annex E.3 independent of whether the UE has an ISIM on the UICC or not (i.e. when the UE has no ISIM SS shall use the same values as if the UE would have an ISIM; furthermore in this case the temporary public user id shall not be included in the set of IMPUs)
22496: NOTE 2:	any arbitrary (but valid) TEL URI
22497: NOTE 3:	According to TS 24.229 clause 5.1.1.1A and 5.1.6.2 [10] when the UE is using ISIM the emergency public user identity is the first public user identity in the list stored in the ISIM; when there is no ISIM it is the default public user id if the UE non-emergency registered with the IM CN and the temporary user id (derived from IMSI) in all other cases.
```

## A.1.4 SUBSCRIBE for reg-event package（行 22498-22771；used_by: TC-011, TC-014）

关键官方标记：`SUBSCRIBE`、`Event`、`reg`、`Security-Verify`、`Expires`

```text
22498: A.1.4	SUBSCRIBE for reg-event package
22499: Header/param
22500: Cond
22501: Value/remark
22502: Rel
22503: Reference
22504: Request-Line
22508: RFC 3261 [15]
22509: 	Method
22511: SUBSCRIBE
22514: 	Request-URI
22516: Public user identity used for subscription (NOTE 2)
22519: 	SIP-Version
22521: SIP/2.0
22524: Route
22526: order of the parameters in this header must be like in the respective rows
22528: RFC 3261 [15]
22529: 	route-param
22530: A1
22531: <sip:SS P-CSCF address:protected server port of P-CSCF;lr>, <sip:scscf.3gpp.org;lr>
22534:       route-param
22535: A2
22536: <sip:SS P-CSCF address: unprotected server port of P-CSCF (optional);lr>, <sip:scscf.3gpp.org;lr>
22539: Via
22543: RFC 3261 [15]
22544: 	sent-protocol
22546: SIP/2.0/UDP  when using UDP or SIP/2.0/TCP  when using TCP
22549: 	sent-by
22550: A1
22551: IP address or FQDN and protected server port of the UE
22554: 	sent-by
22555: A2
22556: IP address or FQDN, port (optional) and not checked
22559: 	via-branch
22561: value starting with 'z9hG4bK'
22564: From
22568: RFC 3261 [15]
22569: 	addr-spec
22571: Public user identity used for subscription (NOTE 2)
22574: 	tag
22576: must be present, value not checked but stored for later reference
22579: To
22583: RFC 3261 [15]
22584: 	addr-spec
22586: Public user identity used for subscription (NOTE 2
22589: 	tag
22591: not present
22594: Contact
22598: RFC 3261 [15]
22599: RFC 5627 [61]
22600: 	addr-spec
22601: A1
22602: SIP URI with IP address or FQDN and protected server port of UE
22605: 	addr-spec
22606: A2
22607: SIP URI with IP address or FQDN and unprotected server port of UE
22610: 	addr-spec
22611: A4
22612: Public GRUU as obtained during registration as pub-gruu contact parameter of the 200 OK for REGISTER response
22615: Expires
22619: RFC 3261 [15]
22620: 	delta-seconds
22622: 600000
22625: Security-Verify
22626: A1
22629: RFC 3329 [21]
22630: 	sec-mechanism
22632: same value as Security Server header sent by SS
22635: Security-Verify
22636: A5
22637: Not present
22640: Require
22641: A1
22644: RFC 3261 [15]
22645: RFC 3329 [21]
22646: 	option-tag
22648: sec-agree
22651: Require
22652: A5
22653: Not present
22656: Proxy-Require
22657: A1
22660: RFC 3261 [15]
22661: RFC 3329 [21]
22662: 	option-tag
22664: sec-agree
22667: Proxy-Require
22668: A5 
22669: Not present
22672: CSeq
22676: RFC 3261 [15]
22677: 	value
22679: value not checked
22682: 	method
22684: SUBSCRIBE
22687: Call-ID
22691: RFC 3261 [15]
22692: 	callid
22694: value not checked, but stored for later reference
22697: Max-Forwards
22701: RFC 3261 [15]
22702: 	value
22704: non-zero value
22707: P-Access-Network-Info
22708: A1, A5
22711: RFC 7315 [132]
22712: 	access-net-spec
22713: A1
22714: access network technology and, if applicable, the cell ID
22717: 	access-net-spec
22718: A5
22719: access network technology for Fixed Broadband and if applicable DSL Location Parameter
22722: Accept 
22724: (if present)
22726: RFC 3261 [15]
22727: RFC 3680 [22]
22728: 	media-range
22730: application/reginfo+xml
22733: Event
22737: RFC 6665 [140]
22738: RFC 3680 [22]
22739: 	event-type
22741: reg
22744: Content-Length
22746: header shall be present if UE uses TCP to send this message and if there is a message-body
22748: RFC 3261 [15]
22749: 	value
22751: length of request body, if such is present
22755: Condition
22756: Explanation
22757: A1
22758: IMS security (A.6a/2 3GPP TS 34.229-2 [5])
22759: A2
22760: GIBA (A.6a/1 3GPP TS 34.229-2 [5])
22761: A3
22762: Void
22763: A4
22764: obtaining and using GRUUs in the Session Initiation Protocol (SIP) (A.4/53 3GPP TS 34.229-2 [5])
22765: A5
22766: SIP Digest without TLS for Fixed Broadband Access (SIP Digest without TLS, A.6a/5 3GPP TS 34.229-2 [5])
22768: NOTE1:	All choices for applicable conditions are described for each header.
22769: NOTE2:	According to TS 24.229 clause 5.1.1.3 the public user identity used for subscription is:
22770: a) when the UE has an ISIM the default public user identity or the public user identity used for initial registration
22771: b) when the UE does not have an ISIM the default public user identity
```

## A.1.5 200 OK for SUBSCRIBE（行 22772-22918；used_by: TC-011, TC-014）

关键官方标记：`SUBSCRIBE`、`200`、`OK`、`Contact`、`Expires`

```text
22772: A.1.5	200 OK for SUBSCRIBE
22773: Header/param
22774: Cond
22775: Value/remark
22776: Rel
22777: Reference
22778: Status-Line
22782: RFC 3261 [15]
22783: 	SIP-Version
22785: SIP/2.0
22788: 	Status-Code
22790: 200
22793: 	Reason-Phrase
22795: OK
22798: Via
22802: RFC 3261 [15]
22803: 	via-parm
22805: same value as received in SUBSCRIBE message
22808: To
22812: RFC 3261 [15]
22813: 	addr-spec
22815: same value as received in SUBSCRIBE message
22818: 	tag
22820: common to-tag (subscribe dialog)
22823: From
22827: RFC 3261 [15]
22828: 	addr-spec
22830: same value as received in SUBSCRIBE message
22833: 	tag
22835: same value as received in SUBSCRIBE message
22838: Call-ID
22842: RFC 3261 [15]
22843: 	callid
22845: same value as received in SUBSCRIBE message
22848: CSeq
22852: RFC 3261 [15]
22853: 	value
22855: same value as received in SUBSCRIBE message
22858: Contact
22862: RFC 3261 [15]
22863: 	addr-spec
22865: <scscf.3gpp.org>
22868: Expires
22872: RFC 3261 [15]
22873: 	delta-seconds
22875: 600000
22878: Record-Route
22882: RFC 3261 [15]
22883: 	addr-spec
22884: A1
22885: SS P-CSCF address: protected server port of SS
22888: 	addr-spec
22889: A2, A3
22890: SS P-CSCF address: unprotected server port of SS (optional) 
22893: 	uri-parameter
22895: lr
22898: Content-Length
22902: RFC 3261 [15]
22903: 	value
22905: 0
22909: Condition
22910: Explanation
22911: A1
22912: IMS security (A.6a/2 3GPP TS 34.229-2 [5])
22913: A2
22914: GIBA (A.6a/1 3GPP TS 34.229-2 [5])
22915: A3
22916: SIP Digest without TLS for Fixed Broadband Access (SIP Digest without TLS, A.6a/5 3GPP TS 34.229-2 [5])
22918: NOTE1:	All choices for applicable conditions are described for each header.
```

## A.1.6 NOTIFY for reg-event package（行 22919-23238；used_by: TC-011, TC-014）

关键官方标记：`NOTIFY`、`Event`、`reg`、`Subscription-State`、`P-Associated-URI`

```text
22919: A.1.6	NOTIFY for reg-event package
22920: Header/param
22921: Cond
22922: Value/remark
22923: Rel
22924: Reference
22925: Request-Line
22929: RFC 3261 [15]
22930: 	Method
22932: NOTIFY
22935: 	Request-URI
22936: A1
22937: same URI as used by the UE in the corresponding REGISTER message and protected server port of UE
22940: 	Request-URI
22941: A2, A5
22942: same URI as used by the UE in the corresponding REGISTER message and unprotected server port of UE
22945: 	SIP-Version
22947: SIP/2.0
22950: Via
22952: order of the parameters in this header must be like in this table
22954: RFC 3261 [15]
22955: 	via-parm1:
22960: 		Sent-protocol
22962: SIP/2.0/UDP  when using UDP or SIP/2.0/TCP  when using TCP
22965: 		sent-by
22966: A1
22967: IP address and protected server port of SS
22970: 		sent-by
22971: A2, A5
22972: IP address and unprotected server port of SS (optional)
22975: 		via-branch
22977: value starting with 'z9hG4bK' (NOTE 4)
22980: 	via-parm2:
22985: 		sent-protocol
22987: SIP/2.0/UDP  when using UDP or SIP/2.0/TCP  when using TCP
22990: 		sent-by
22992: scscf.3gpp.org
22995: 		via-branch	
22997: value starting with 'z9hG4bK' (NOTE 4)
23000: From
23004: RFC 3261 [15]
23005: 	addr-spec
23007: same URI as received in the To header of the previous SUBSCRIBE message (NOTE 3)
23010: 	tag
23012: common to-tag (subscribe dialog)
23015: To
23019: RFC 3261 [15]
23020: 	addr-spec
23022: same URI as received in the From header of the previous SUBSCRIBE message (NOTE 3)
23025: 	tag	
23027: same value as received in From tag of SUBSCRIBE message
23030: Call-ID
23034: RFC 3261 [15]
23035: 	callid
23037: same as value received in SUBSCRIBE message
23040: CSeq
23041: A1, A2, A5
23044: RFC 3261 [15]
23045: 	value
23047: 1
23050: 	method
23052: NOTIFY
23055: Contact
23059: RFC 3261 [15]
23060: 	addr-spec
23062: <sip:scscf.3gpp.org>
23065: Content-Type
23069: RFC 3261 [15]
23070: RFC 3680 [22]
23071: 	media-type
23073: application/reginfo+xml
23076: Event
23077: A1, A2, A5
23080: RFC 6665[140]
23081: RFC 3680 [22]
23082: 	event-type
23084: reg
23087: Max-Forwards
23091: RFC 3261 [15]
23092: 	value
23094: 69
23097: Subscription-State
23101: RFC 6665 [140]
23102: 	substate-value
23104: active
23107: 	expires
23109: 600000
23112: Content-Length
23116: RFC 3261 [15]
23117: RFC 3680 [22]
23118: 	value
23120: length of message-body
23123: Message-body
23124: A3
23125: <?xml version="1.0" encoding="UTF-8"?>
23126: <reginfo xmlns="urn:ietf:params:xml:ns:reginfo" version="0" state="full">
23127: <registration aor="PublicUserIdentity1 (NOTE 2)" id="a100" state="active">
23128:     <contact id="980" state="active" event="registered">
23129:     <uri>same value as in Contact header of REGISTER request</uri>
23130:     </contact>
23131: </registration>
23132: <registration aor="AssociatedTelUri (NOTE 2)" id="a101" state="active">
23133:     <contact id="981" state="active" event="created">
23134:     <uri>same value as in Contact header of REGISTER request</uri>
23135:     </contact>
23136: </registration>
23137: <registration aor="PublicUserIdentity2 (NOTE 2)" id="a102" state="active">
23138:     <contact id="982" state="active" event="registered">
23139:     <uri>same value as in Contact header of REGISTER request</uri>
23140:     </contact>
23141: </registration>
23142: <registration aor="PublicUserIdentity3 (NOTE 2)" id="a103" state="active">
23143:     <contact id="983" state="active" event="registered">
23144:     <uri>same value as in Contact header of REGISTER request</uri>
23145:     </contact>
23146: </registration>
23147: </reginfo>
23151: A4
23152: <?xml version="1.0" encoding="UTF-8"?>
23153: <reginfo xmlns="urn:ietf:params:xml:ns:reginfo" xmlns:gr="urn:ietf:params:xml:ns:gruuinfo" version="0" state="full">
23155: <registration aor="PublicUserIdentity1 (NOTE 2)" id="a100" state="active">
23156: <contact id="980" state="active" event="registered" callid="Call-Id of most recent REGISTER" cseq="CSeq value of most recent REGISTER">
23157: <uri>same value as in Contact header of REGISTER request</uri>
23158: <unknown-param name="+sip.instance">
23159: "Instance ID of the UE;"
23160: </unknown-param>
23161: <gr:pub-gruu uri="public GRUU associated to this aor"/>
23162: <gr:temp-gruu uri="temporary GRUU associated to this aor" first-cseq="CSeq of the REGISTER request that caused the temporary GRUU to assigned for the UE"/>
23163: </contact>
23164: </registration>
23166: <registration aor="AssociatedTelUri (NOTE 2)" id="a101" state="active">
23167: <contact id="981" state="active" event="created"><uri>same value as in Contact header of REGISTER request</uri>
23168: <unknown-param name="+sip.instance">
23169: "Instance ID of the UE;"
23170: </unknown-param>
23171: <gr:pub-gruu uri=" same public GRUU as for PublicUserIdentity1"/>
23172: <gr:temp-gruu uri=" same temporary GRUU as for PublicUserIdentity1" first-cseq="CSeq of the REGISTER request that caused the temporary GRUU to assigned for the UE"/>
23173: </contact>
23174: </registration>
23176: <registration aor="PublicUserIdentity2 (NOTE 2)" id="a102" state="active">
23177: <contact id="982" state="active" event="registered" callid="Call-Id of most recent REGISTER" cseq="CSeq value of most recent REGISTER">
23178: <uri>same value as in Contact header of REGISTER request</uri>
23179: <unknown-param name="+sip.instance">
23180: "Instance ID of the UE;"
23181: </unknown-param>
23182: <gr:pub-gruu uri="public GRUU associated to this aor"/>
23183: <gr:temp-gruu uri="temporary GRUU associated to this aor" first-cseq="CSeq of the REGISTER request that caused the temporary GRUU to assigned for the UE"/>
23184: </contact>
23185: </registration>
23187: <registration aor="PublicUserIdentity3 (NOTE 2)" id="a103" state="active">
23188: <contact id="983" state="active" event="registered" callid="Call-Id of most recent REGISTER" cseq="CSeq value of most recent REGISTER">
23189: <uri>same value as in Contact header of REGISTER request</uri>
23190: <unknown-param name="+sip.instance">
23191: "Instance ID of the UE;"
23192: </unknown-param>
23193: <gr:pub-gruu uri="public GRUU associated to this aor"/>
23194: <gr:temp-gruu uri="temporary GRUU associated to this aor" first-cseq="CSeq of the REGISTER request that caused the temporary GRUU to assigned for the UE"/>
23195: </contact>
23196: </registration>
23197: </reginfo>
23199: RFC 5628 [62]
23200: Message-body
23201: A5
23202: <?xml version="1.0" encoding="UTF-8"?>
23203: <reginfo xmlns="urn:ietf:params:xml:ns:reginfo" version="0" state="full">
23204: <registration aor="PublicUserIdentity1 (NOTE 2)" id="a100" state="active">
23205:     <contact id="980" state="active" event="registered">
23206:     <uri>same value as in Contact header of REGISTER request</uri>
23207:     </contact>
23208: </registration>
23209: <registration aor="AssociatedTelUri (NOTE 2)" id="a101" state="active">
23210:     <contact id="981" state="active" event="created">
23211:     <uri>same value as in Contact header of REGISTER request</uri>
23212:     </contact>
23213: </registration>
23214: </reginfo>
23218: Condition
23219: Explanation
23220: A1
23221: IMS security (A.6a/2 3GPP TS 34.229-2 [5])
23222: A2
23223: GIBA (A.6a/1 3GPP TS 34.229-2 [5]
23224: A3
23225: NOT obtaining and using GRUUs in the Session Initiation Protocol (SIP) (A.4/53 3GPP TS 34.229-2 [5])
23226: A4
23227: obtaining and using GRUUs in the Session Initiation Protocol (SIP) (A.4/53 3GPP TS 34.229-2 [5])
23228: A5
23229: SIP Digest without TLS for Fixed Broadband Access (SIP Digest without TLS, A.6a/5 3GPP TS 34.229-2 [5])
23232: NOTE 1:	All choices for applicable conditions are described for each header.
23233: NOTE 2:	The public user ids and the associated TEL URI are as returned to the UE in the P-Associated-URI header of the 200 (OK) response to the REGISTER request;
23234: PublicUserId1 is the default public user id i.e. the first one contained in P-Associated-URI;
23235: AssociatedTelUri is the same as used in P-Associated-URI
23236: PublicUserId2 and PublicUserId3 are the remaining IMPUs of the P-Associated-URI header
23237: NOTE 3:	This results in using the public user identity used for subscription as defined in TS 24.229 clause 5.1.1.3.
23238: NOTE 4:	Branch parameter values sent by SS are different within a test case execution.
```

## A.1.7 423 Interval Too Brief for REGISTER（行 23239-23312；used_by: TC-011, TC-014）

关键官方标记：`423`、`Interval Too Brief`、`Min-Expires`

```text
23239: A.1.7	423 Interval Too Brief for REGISTER
23240: Header/param
23241: Value/remark
23242: Rel
23243: Reference
23244: Status-Line
23247: RFC 3261 [15]
23248: 	SIP-Version
23249: SIP/2.0
23252: 	Status-Code
23253: 423
23256: 	Reason-Phrase
23257: Interval Too Brief
23260: Via
23263: RFC 3261 [15]
23264: 	via-parm
23265: same value as received in REGISTER message
23268: To
23271: RFC 3261 [15]
23272: 	addr-spec
23273: same value as received in REGISTER message
23276: 	tag
23277: common to-tag (register)
23280: From
23283: RFC 3261 [15]
23284: 	addr-spec
23285: same value as received in REGISTER message
23288: Call-ID
23291: RFC 3261 [15]
23292: 	callid
23293: same value as received in REGISTER message
23296: CSeq
23299: RFC 3261 [15]
23300: 	value
23301: same value as received in REGISTER message
23304: Min-Expires
23307: RFC 3261 [15]
23308: 	delta-seconds
23309: T (a decimal integer number of seconds from 0 to (2**32)-1)
```

> 状态：官方 Annex A 默认消息内容已锚定，作为 TC-011/TC-014 的 `.3.3` 等价骨架；正式一致性判定仍需 SS/一致性仪表按 34.229-1 8.1/8.2 对表执行。

# TC-012/017/019/020/021 官方 TP 过程原文

来源：`3GPP TS 34.229-1` V14.7.0 (2019-06)，逐行抽取自 `<standards-extract>\34229-1e70-word.txt`；行号口径 `Python str.splitlines()` 的 1-based 索引。

抽取范围：每个官方条目的 `Test purpose`、`Method of test`、`Expected sequence`、`Specific Message Contents` 和 `Test requirements`。本文件只固化规范原文，不把本地执行结果升级为官方一致性 PASS。

## 12.12.3-12.12.5 MO MTSI Voice Call Successful with preconditions（行 6314-6360；used_by: TC-012, TC-017）

关键官方标记：`12.12.3	Test purpose`、`12.12.4	Method of test`、`Expected sequence`、`Specific Message Contents`、`12.12.5	Test requirements`、`BYE`、`200 OK`

```text
6314: 12.12.3	Test purpose
6315: 1)	To verify that when initiating MO call the UE performs correct exchange of SIP protocol signalling messages for setting up the session; and
6316: 2)	To verify that within SIP signalling the UE performs the correct exchange of SDP messages for negotiating media and indicating preconditions for resource reservation (as described by 3GPP TS 24.229 [10], clause 6.1).
6317: 3)	To verify that the UE is able to release the call.
6318: 12.12.4	Method of test
6319: Initial conditions
6320: UE contains either SIM application (GIBA), ISIM and USIM applications or only USIM application on UICC. UE has discovered P-CSCF and registered to IMS services, by executing the generic test procedure in Annex C.2 or C.2a (GIBA only) up to the last step.
6321: SS is configured with the shared secret key of IMS AKA algorithm, related to the IMS private user identity (IMPI) configured on the UICC card equipped into the UE. SS has performed AKAv1-MD5 authentication with the UE and accepted the registration (IMS security).
6322: Test procedure applicable for a UE with E-UTRA support (TS 34.229-2 [5] A.18/1)
6323: 1-14)	UE executes the procedures described in TS 36.508 [94] table 4.5A.6.3-1 steps 1 to14.
6324: Expected sequence
6325: NOTE:	Only the IMS procedure relevant to the test purpose is described below.
6326: Step
6327: Direction
6328: Message
6329: Comment
6331: UE
6332: SS
6335: 1-13
6337: Steps defined in annex C.21
6338: MTSI MO speech call. Referred from 36.508 [94] table 4.5A.6.3-1 for a UE with E-UTRA support.
6339: 13A
6341: The UE is triggered by MMI to release the call
6343: 14
6344: -->
6345: BYE
6346: The UE releases the call with BYE
6347: 15
6348: <--
6349: 200 OK
6350: The SS sends 200 OK for BYE
6352: Specific Message Contents
6353: Steps 1 - 13 as specified in annex C.21
6354: BYE (Step 14)
6355: Use the default message "BYE" in annex A.2.8.
6356: 200 OK for BYE (Step 15)
6357: Use the default message "200 OK for other requests than REGISTER or SUBSCRIBE" in annex A.3.1.
6358: 12.12.5	Test requirements
6359: SS must check that if the UE uses IMS security, it sends all the requests over the security associations set up during registration, in accordance to 3GPP TS 24.229 [10], clause 5.1.1.5.1.
6360: Step 14: the UE shall send a BYE request with the correct content, according to common message definitions.
```

## 12.12a.3-12.12a.5 MO MTSI Voice Call Successful without preconditions（行 6390-6529；used_by: TC-012, TC-017）

关键官方标记：`12.12a.3	Test purpose`、`12.12a.4	Method of test`、`Expected sequence`、`Specific Message Contents`、`a=rtpmap`、`BYE`、`200 OK`

```text
6390: 12.12a.3	Test purpose
6391: 1)	To verify that when initiating MO call the UE performs correct exchange of SIP protocol signalling messages for setting up the session; and
6392: 2)	To verify that UE performs the correct exchange of SDP messages for negotiating media without using preconditions. 
6393: 3)	To verify that the UE is able to release the call.
6394: 12.12a.4	Method of test
6395: Initial conditions
6396: UE contains either SIM application (GIBA), ISIM and USIM applications or only USIM application on UICC. UE has discovered P-CSCF and registered to IMS services, by executing the generic test procedure in Annex C.2 or C.2a (GIBA only) up to the last step.
6397: SS is configured with the shared secret key of IMS AKA algorithm, related to the IMS private user identity (IMPI) configured on the UICC card equipped into the UE. SS has performed AKAv1-MD5 authentication with the UE and accepted the registration (IMS security).  UE is configured to not use the precondition mechanism.
6398: Test procedure applicable for a UE with E-UTRA support (TS 34.229-2 [5] A.18/1)
6399: 1-14)	UE executes the procedures described in TS 36.508 [94] table 4.5A.6.3-1 steps 1 to 14.
6400: Expected sequence
6401: NOTE:	Only the IMS procedure relevant to the test purpose is described below.
6402: Step
6403: Direction
6404: Message
6405: Comment
6407: UE
6408: SS
6411: 1-6
6413: Steps 1-6 defined in annex C.21
6414: MTSI MO speech call. Referred from 36.508 [94] table 4.5A.6.3-1 for a UE with E-UTRA support.
6415: 7
6417: Step 9 defined in annex C.21
6418: SS sends a 180 Ringing 
6419: 8-9
6421: Steps 12-13 defined in annex C.21
6422: SS sends 200 OK for INVITE and UE acknowledges 
6423: 10
6424: -->
6425: BYE
6426: The UE releases the call with BYE
6427: 11
6428: <--
6429: 200 OK
6430: The SS sends 200 OK for BYE
6432: Specific Message Contents
6433: Steps 1 - 6,9 and 12-13 as specified in annex C.21 with the following exceptions:
6434: INVITE (Step 2)
6435: Use the default message "INVITE for MO Call" in annex A.2.1 with the following exceptions:
6436: Message-body
6437: The following SDP types and values.
6439: Session description:
6440: -	v=0
6441: -	o=(username) (sess-id) (sess-version) IN (addrtype) (unicast-address for UE)
6442: -	s=(session name)
6443: -	c=IN (addrtype) (connection-address for UE) [Note 1]
6444: -	b=AS: (bandwidth-value)
6446: Time description:
6447: -	t= (start-time) (stop-time)
6449: Media description:
6450: -	m=audio (transport port) RTP/AVP (fmt)
6451: -	c=IN (addrtype) (connection-address for UE) [Note 1]
6452: -	b=AS: (bandwidth-value)
6453: -	b=RS: (bandwidth-value) [Note 4]
6454: -	b=RR: (bandwidth-value) [Note 4]
6456: Attributes for media: 
6457: -	a=rtpmap: (payload type) AMR-WB/16000 [Note 5]
6458: -	a=fmtp: (format) mode-change-capability=2; max-red= (att-field) [Note 6, 7]
6459: -	a=rtpmap: (payload type) telephone-event/16000
6460: -	a=fmtp: (format) 
6461: -	a=rtpmap: (payload type) AMR/8000 [Note 5]
6462: -	a=fmtp: (format) mode-change-capability=2; max-red= (att-field) [Note 6, 7]
6463: -	a=rtpmap: (payload type) telephone-event/8000 
6464: -	a=fmtp: (format) 
6465: -	a=ecn-capable-rtp: leap ect=0 [Note 2]
6466: -	a=rtcp-fb:* nack ecn [Note 2]
6467: -	a=rtcp-xr:ecn-sum [Note 2]
6468: -	a=rtcp-rsize [Note 2]
6469: -	a=ptime:20
6470: -	a=maxptime:240
6471: Attributes for media security mechanism:
6472: -	a=3ge2ae: requested [Note 3]
6473: -	a=crypto:1 AES_CM_128_HMAC_SHA1_80inline:WVNfX19zZW1jdGwgKCkgewkyMjA7fQp9CnVubGVz|2^20|
6474: 1:4FEC_ORDER=FEC_SRTP" [Note 3]
6476: Note 1: At least one "c=" field shall be present.
6477: Note 2: Attributes for ECN Capability may be present if the UE supports Explicit Congestion Notification.
6478: Note 3: Attributes for media plane security are present if the use of end-to-access-edge security is supported by UE.
6479: Note 4: The RR value must be greater than 0. The RS value can be any value.
6480: Note 5: The AMR channel number shall be "/1" or omitted.
6481: Note 6: The max-red values from 0 to 220 are allowed.
6482: Note 7: The parameters mode-set, mode-change-period, mode-change-neighbor, crc, robust-sorting and interleaving shall not be included.
6484: 183 Session Progress (Step 4)
6485: Use the default message "183 Session Progress" in annex A.2.3 with the following exceptions:
6486: Message-body
6487: The following SDP types and values.
6489: Session description:
6490: -	v=0
6491: -	o=- 1111111111 1111111111 IN (addrtype) (unicast-address for SS)
6492: -	s=-
6493: -	c=IN (addrtype) (connection-address for SS)
6494: -	b=AS:37
6496: Time description:
6497: -	t=0 0
6499: Media description:
6500: -	m=audio (transport port) RTP/AVP (fmt) [Note 1, 4]
6501: -	b=AS:37
6502: -	b=RS: (bandwidth-value) [Note 5]
6503: -	b=RR: (bandwidth-value) [Note 5]
6505: Attributes for media:
6506: -	a=rtpmap: (payload type) AMR-WB/16000/1 [Note 1]
6507: -	a=fmtp: (format) mode-change-capability=2; max-red=220 [Note 1]
6508: -	a=ecn-capable-rtp: leap ect=0 [Note 2]
6509: -	a=rtcp-fb:* nack ecn [Note 2]
6510: -	a=rtcp-xr:ecn-sum [Note 2]
6511: -	a=ptime:20
6512: -	a=maxptime:240
6514: Attributes for media security mechanism:
6515: -	a=3ge2ae: requested [Note 3]
6516: -	a=crypto:1 AES_CM_128_HMAC_SHA1_80inline:PS1uQCVeeCFCanVmcjkpPywjNWhcYD0mXXtxaVBR|2^20|1:4 [Note 3]
6518: Note 1: The value for fmt, payload type (AMR) and format is copied from step 2.
6519: Note 2: Attributes for ECN Capability are present if the UE supports Explicit Congestion Notification.
6520: Note 3: Attributes for media plane security are present if the use of end-to-access-edge security is supported by UE.
6521: Note 4: transport port is the port number of the SS (see RFC 3264 clause 6).
6522: Note 5: The bandwidth-value is copied from step 2.
6524: 180 Ringing (Step 7)
6525: Use the default message "180 Ringing for INVITE" in annex A.2.6 applying condition A1 (in addition to any other applicable conditions).
6526: BYE (Step 10)
6527: Use the default message "BYE" in annex A.2.8.
6528: 200 OK for BYE (Step 11)
6529: Use the default message "200 OK for other requests than REGISTER or SUBSCRIBE" in annex A.3.1.
```

## 12.13.3-12.13.5 MT MTSI speech call with preconditions（行 6561-6592；used_by: TC-019）

关键官方标记：`12.13.3	Test purpose`、`12.13.4	Method of test`、`Expected sequence`、`Specific Message Content`、`12.13.5	Test requirements`

```text
6561: 12.13.3	Test purpose
6562: 1)	To verify that, when initiating MT MTSI speech call and SS needs to reserve resources, the UE performs correct exchange of SIP protocol signalling messages for setting up the session.
6563: 2)	To verify that within SIP signalling the UE performs the correct exchange of SIP header and parameter contents.
6564: 3)	To verify that within SIP signalling the UE performs the correct exchange of SDP contents.
6565: 4)	To verify that the UE is able to release the call.
6566: 12.13.4	Method of test
6567: Initial conditions
6568: UE contains either ISIM and USIM applications or only USIM application on UICC. UE has discovered P-CSCF and registered to IMS services, by executing the generic test procedure in Annex C.2 or C.2a (GIBA only) up to the last step.
6569: SS is configured with the shared secret key of IMS AKA algorithm, related to the IMS private user identity (IMPI) configured on the UICC card equipp5ed into the UE. SS has performed AKAv1-MD5 authentication with the UE and accepted the registration (IMS security).
6570: Test procedure applicable for a UE with E-UTRA support (TS 34.229-2 [5] A.18/1)
6571: 1-26)	UE executes the procedures described in TS 36.508 [94] table 4.5A.7.3-1 steps 1 to26.
6572: Expected sequence
6573: NOTE:	Only the IMS procedure relevant to the test purpose is described below.
6574: Step
6575: Direction
6576: Message
6577: Comment
6579: UE
6580: SS
6583: 1-15
6585: Steps defined in annex C.11
6586: MTSI MT speech call. Referred from 36.508 [94] table 4.5A.7.3-1 for a UE with E-UTRA support.
6588: NOTE:	The default messages contents in annex A are used with condition "IMS security" or "GIBA" when applicable
6589: Specific Message Content
6590: None.
6591: 12.13.5	Test requirements
6592: The UE shall send requests and responses as described in clause 12.13.4
```

## 12.13a.3-12.13a.5 MT MTSI speech call when remote end reserves resources before INVITE（行 6622-6744；used_by: TC-019）

关键官方标记：`12.13a.3	Test purpose`、`12.13a.4	Method of test`、`Expected sequence`、`Specific Message Content`、`12.13a.5	Test requirements`

```text
6622: 12.13a.3	Test purpose
6623: 1)	To verify that, when initiating MT MTSI speech call and remote end does not need to reserve resources, the UE performs correct exchange of SIP protocol signalling messages for setting up the session.
6624: 2)	To verify that within SIP signalling the UE performs the correct exchange of SIP header and parameter contents.
6625: 3)	To verify that within SIP signalling the UE performs the correct exchange of SDP contents.
6626: 12.13a.4	Method of test
6627: Initial conditions
6628: UE contains either ISIM and USIM applications or only USIM application on UICC. UE has discovered P-CSCF and registered to IMS services, by executing the generic test procedure in Annex C.2 or C.2a (GIBA only) up to the last step.
6629: SS is configured with the shared secret key of IMS AKA algorithm, related to the IMS private user identity (IMPI) configured on the UICC card equipped into the UE. SS has performed AKAv1-MD5 authentication with the UE and accepted the registration (IMS security).
6630: Test procedure applicable for a UE with E-UTRA support (TS 34.229-2 [5] A.18/1)
6631: Expected sequence
6632: NOTE:	Only the IMS procedure relevant to the test purpose is described below.
6633: Step
6634: Direction
6635: Message
6636: Comment
6638: UE
6639: SS
6642: 1-6
6644: Steps 1-6 defined in annex C.11
6646: 7-13
6648: Steps 9-15 defined in annex C.11
6651: NOTE:	The default messages contents in annex A are used with condition "IMS security" or "GIBA" when applicable
6652: Specific Message Content
6653: INVITE (Step 1)
6654: Use the default message "INVITE for MT Call" in annex A.2.9 with the following exceptions:
6655: Header/param
6656: Value/remark
6657: Supported
6659:    option-tag
6660: precondition
6661: Message-body
6662: The following SDP types and values.
6664: Session description:
6665: - v=0
6666: - o=- 1111111111 1111111111 IN (addrtype) (unicast-address for SS)
6667: - s=-
6668: - c=IN (addrtype) (connection-address for SS)
6669: - b=AS:37
6671: Time description:
6672: - t=0 0
6674: Media description:
6675: - m=audio (transport port) RTP/AVP 97 98 99 100
6676: - b=AS:37
6677: - b=RS:0
6678: - b=RR:2000
6680: Attributes for media: 
6681: - a=rtpmap:97 AMR-WB/16000/1
6682: - a=fmtp:97 mode-change-capability=2; max-red=220
6683: - a=rtpmap: 98 telephone-event/16000
6684: - a=fmtp: 98 0-15
6685: - a=rtpmap:99 AMR/8000/1
6686: - a=fmtp:99 mode-change-capability=2; max-red=220
6687: - a=rtpmap: 100 telephone-event/8000
6688: - a=fmtp: 100 0-15
6689: - a=ptime:20
6690: - a=maxptime:240
6692: Attributes for preconditions:
6693: - a=curr:qos local sendrecv
6694: - a=curr:qos remote none
6695: - a=des:qos mandatory local sendrecv
6696: - a=des:qos optional remote sendrecv
6698: 183 Session Progress (Step 4)
6699: Use the default message "183 Session Progress" in annex A.2.3 with the following exceptions:
6700: Header/param
6701: Value/remark
6702: Status-Line
6704:     Reason-Phrase
6705: Not checked
6706: Require
6708:    option-tag
6709: precondition
6710: Message-body
6711: The following SDP types and values shall be present.
6713: Session description:
6714: - v=0
6715: - o=(user-name) (sess-id) (sess-version) IN (addrtype) (unicast-address for UE)
6716: - s=(session name)
6717: - c=IN (addrtype) (connection-address for UE) [Note 1]
6718: - b=AS: (bandwidth-value)
6720: Time description:
6721: - t=0 0
6723: Media description:
6724: - m=audio (transport port) RTP/AVP (fmt) [Note 2]
6725: - c=IN (addrtype) (connection-address for UE) [Note 1]
6726: - b=AS: (bandwidth-value)
6727: - b=RS: (bandwidth-value)
6728: - b=RR: (bandwidth-value)
6730: Attributes for media:
6731: - a=rtpmap:(payload type) AMR-WB/16000 [Note 2]
6732: - a=fmtp:(format) [Note 2, 3]
6734: Attributes for preconditions:
6735: - a=curr:qos local none or a=curr:qos local sendrecv
6736: - a=curr:qos remote sendrecv
6737: - a=des:qos mandatory local sendrecv
6738: - a=des:qos mandatory remote sendrecv
6739: Note 1: At least one "c=" field shall be present.
6740: Note 2: The value for fmt, payload type and format is not checked
6741: Note 3: Parameters for the AMR codec are not checked
6743: 12.13a.5	Test requirements
6744: The UE shall send requests and responses as described in clause 12.13a.4.
```

## 15.11.3-15.11.5 MO Call Hold without announcement（行 9759-9824；used_by: TC-020）

关键官方标记：`15.11.3	Test purpose`、`15.11.4	Method of test`、`Expected sequence`、`Specific Message Contents`、`15.11.5	Test requirements`

```text
9759: 15.11.3	Test purpose
9760: 1)	To verify that the invoking UE puts the call on hold with a correct exchange of SIP/SDP protocol signalling messages; and
9761: 2)	To verify that the invoking UE is able to resume the call with a correct exchange of SIP/SDP protocol signalling messages.
9762: 15.11.4	Method of test
9763: Initial conditions
9764: UE contains either ISIM and USIM applications or only USIM application on UICC. UE has discovered P-CSCF, registered to IMS services and set up the MO call, by executing the generic test procedure in Annex C.2 or C.2a (GIBA only) up to the last step and thereafter executing the generic test procedure in TS 36.508 [94] table 4.5A.6.3-1 steps 1 to 14 for a UE with E-UTRA support (TS 34.229-2 [5] A.18/1).
9765: SS is configured with the shared secret key of IMS AKA algorithm, related to the IMS private user identity (IMPI) configured on the UICC card equipped into the UE. SS has performed AKAv1-MD5 authentication with the UE and accepted the registration and MO call.
9766: Test procedure
9767: 1)	Call hold is initiated on the UE. SS waits for the UE to send an INVITE or UPDATE request with a SDP offer
9768: 2)	If the UE sent an INVITE request in step 1, SS responds to it with a 100 Trying response. No such response is sent for UPDATE.
9769: 3)	SS responds to the INVITE or UPDATE request with a valid 200 OK response.
9770: 4)	If the UE sent an INVITE request in step 1, SS waits for the UE to send an ACK to acknowledge receipt of the 200 OK for INVITE.
9771: 5)	Call resume is initiated on the UE. SS waits for the UE to send an INVITE or UPDATE request with a SDP offer
9772: 6)	If the UE sent an INVITE request in step 5, SS responds to it with a 100 Trying response. No such response is sent for UPDATE.
9773: 7)	SS responds to the INVITE or UPDATE request with a valid 200 OK response.
9774: 8)	If the UE sent an INVITE in step 5, SS waits for the UE to send an ACK to acknowledge receipt of the 200 OK for INVITE.
9775: 9)	Call is released on the UE. SS waits for the UE to send a BYE request.
9776: 10)	SS responds to the BYE request with valid a 200 OK response.
9777: Expected sequence
9778: Step
9779: Direction
9780: Message
9781: Comment
9783: UE
9784: SS
9789: User initiates holding the call 
9791: 1-4
9793: Steps 1-4 specified in annex C.8 to hold the call
9797: User initiates resuming the call
9799: 5-8
9801: Steps 1-4 specified in annex C.8 to resume the call
9805: User initiates releasing the call
9807: 9
9808: -->
9809: BYE
9810: The UE releases the call with BYE
9811: 10
9812: <--
9813: 200 OK
9814: The SS sends 200 OK for BYE
9816: Specific Message Contents
9817: Messages in Step 1-4
9818: Use messages according to annex C.8 to put the call on hold.
9819: Messages in Step 5-8
9820: Use messages according to annex C.8 to resume the call.
9821: 15.11.5	Test requirements
9822: SS must check that if the UE uses IMS security, it sends all the requests over the security associations set up during registration, in accordance to 3GPP TS 24.229 [10], clause 5.1.1.5.1.
9823: Step 1: the UE shall send an INVITE or UPDATE request with correct content. The UE shall include the same lines in the SDP body as specified call hold in step 1 of annex C.8.
9824: Step 5: the UE shall send an INVITE or UPDATE request with correct content. The UE shall include the same lines in the SDP body as specified for call resume in step 1 of annex C.8.
```

## 15.12.3-15.12.5 MT Call Hold without announcement（行 9935-9985；used_by: TC-020）

关键官方标记：`15.12.3	Test purpose`、`15.12.4	Method of test`、`Expected sequence`、`Specific Message Contents`、`15.12.5	Test requirements`

```text
9935: 15.12.3	Test purpose
9936: 1)	To verify that the held UE responds correctly to call hold and resume requests from SS.
9937: 15.12.4	Method of test
9938: Initial conditions
9939: UE contains either ISIM and USIM applications or only USIM application on UICC. UE has discovered P-CSCF, registered to IMS services and set up the MO call, by executing the generic test procedure in Annex C.2 or C.2a (GIBA only) up to the last step and thereafter executing the generic test procedure in TS 36.508 [94] table 4.5A.6.3-1 steps 1 to 14 for a UE with E-UTRA support (TS 34.229-2 [5] A.18/1).
9940: SS is configured with the shared secret key of IMS AKA algorithm, related to the IMS private user identity (IMPI) configured on the UICC card equipped into the UE. SS has performed AKAv1-MD5 authentication with the UE and accepted the registration and MO call.
9941: Test procedure
9942: 1)	SS initiates the call hold by sending a re-INVITE to set the media streams into sendonly state.
9943: 2)	Optional: SS waits for the UE to respond to the INVITE request with a 100 Trying response.
9944: 3)	SS waits for the UE to respond to the INVITE request with valid 200 OK response.
9945: 4)	SS sends an ACK to acknowledge receipt of the 200 OK for INVITE.
9946: 5)	SS resumes the call by sending another re-INVITE request with a SDP offer to set the media streams into sendrecv state again.
9947: 6)	Optional: SS waits for the UE to respond to the INVITE request with a 100 Trying response.
9948: 7)	SS waits for the UE to respond to the INVITE request with valid 200 OK response.
9949: 8)	SS sends an ACK to acknowledge receipt of the 200 OK for INVITE.
9950: 9)	SS sends a BYE request to the UE in order to release the call.
9951: 10)	UE responds to the BYE request with valid 200 OK response.
9952: Expected sequence
9953: Step
9954: Direction
9955: Message
9956: Comment
9958: UE
9959: SS
9962: 1-4
9964: Steps 1-4 specified in annex C.9 to hold the call
9966: 5-8
9968: Steps 1-4 specified in annex C.9 to resume the call
9970: 9
9971: <--
9972: BYE
9973: The SS releases the call with BYE
9974: 10
9975: -->
9976: 200 OK
9977: The UE sends 200 OK for BYE
9979: Specific Message Contents
9980: BYE (Step 9)
9981: Use the default message "BYE" in annex A.2.8.
9982: 200 OK for BYE (Step 10)
9983: Use the default message "200 OK for other requests than REGISTER or SUBSCRIBE" in annex A.3.1.
9984: 15.12.5	Test requirements
9985: SS must check that the UE correctly responds to all the mid-dialog INVITEs sent by the SS.
```

## 15.17.3-15.17.5 Creating and leaving a conference（行 10495-10564；used_by: TC-021）

关键官方标记：`15.17.3	Test purpose`、`15.17.4	Method of test`、`Expected sequence`、`Specific Message Contents`、`15.17.5	Test requirements`

```text
10495: 15.17.3	Test purpose
10496: 1)	To verify that when creating a conference with conference factory URI the UE performs correct exchange of SIP protocol signalling messages with the conference factory; and
10497: 2)	To verify that within SIP signalling the UE performs the correct exchange of SDP messages for negotiating media and indicating preconditions for resource reservation (as described by 3GPP TS 24.229 [10], clause 6.1).
10498: 3)	To verify the correct SIP message exchange if the UE optionally subscribes to the conference event package.
10499: 15.17.4	Method of test
10500: Initial conditions
10501: UE contains either SIM application (GIBA), ISIM and USIM applications or only USIM application on UICC. UE has activated a PDP context, discovered P-CSCF and registered to IMS services, by executing the generic test procedure in Annex C.2 or C.2a (GIBA only) up to the last step.
10502: SS is configured with the shared secret key of IMS AKA algorithm, related to the IMS private user identity (IMPI) configured on the UICC card equipped into the UE. SS has performed AKAv1-MD5 authentication with the UE and accepted the registration (IMS security).
10503: Test procedure
10504: 1-13)	UE executes the procedures described in TS 36.508 [94] table 4.5A.6.3-1 steps 1 to14)
10505: 13A)	UE is triggered to leave the conference.
10506: 14)	UE leaves the created conference. SS waits the UE to send a BYE request.
10507: 15)	SS responds to the BYE request with valid 200 OK response.
10508: 16)	SS notifies the UE that its subscription to conf event is terminated.
10509: 17)	UE responds with 200 OK.
10510: Expected sequence
10511: Step
10512: Direction
10513: Message
10514: Comment
10516: UE
10517: SS
10520: 1-13
10522: Steps defined in annex C.10
10523: MTSI conference call created
10524: 13A
10527: Make UE leave the conference
10528: 14
10529: -->
10530: BYE
10531: The UE leaves the conference with BYE
10532: 15
10533: <--
10534: 200 OK
10535: The SS sends 200 OK for BYE
10536: 16
10537: <--
10538: NOTIFY
10539: If the UE had subscribed to the conference event package, the SS notifies the UE that its subscription to conference event package is terminated
10540: 17
10541: -->
10542: 200 OK
10543: The UE sends 200 OK for NOTIFY (if sent by SS)
10545: NOTE:	The default messages contents in annex A are used with condition "IMS security" or "GIBA" when applicable
10546: Specific Message Contents
10547: Specific Message contents for Steps 1 - 13 as specified in annex C.10
10548: BYE (Step 14)
10549: Use the default message "BYE" in annex A.2.8 but with the following exceptions:
10550: Header/param
10551: Value/remark
10552: Request-Line
10554: 	Request-URI
10555: sip:final@conf-factory. appended with px_IMS_HomeDomainName
10557: 200 OK for BYE (Step 15)
10558: Use the default message "200 OK for other requests than REGISTER or SUBSCRIBE" in annex A.3.1.
10559: NOTIFY (Step 16)
10560: Use the default message "NOTIFY for conference event package" in annex A.5.3 with condition A4.
10561: 200 OK for NOTIFY (Step 15)
10562: Use the default message "200 OK for other requests than REGISTER or SUBSCRIBE" in annex A.3.1.
10563: 15.17.5	Test requirements
10564: SS must check that if the UE uses IMS security, it sends all the requests over the security associations set up during registration, in accordance to 3GPP TS 24.229 [10], clause 5.1.1.5.1.
```

## 15.18.3-15.18.5 Inviting user to conference by sending REFER to the user（行 10579-10721；used_by: TC-021）

关键官方标记：`15.18.3	Test purpose`、`15.18.4	Method of test`、`Expected sequence`、`Specific Message Contents`、`15.18.5	Test requirements`、`REFER`、`NOTIFY`

```text
10579: 15.18.3	Test purpose
10580: 1)	To verify that the UE sends a correctly composed REFER request to invite a user to conference; and
10581: 2)	To verify that the UE correctly processes the NOTIFYs from the invited user; and
10582: 3)	To verify that the UE correctly processes the NOTIFYs for the conference event package if the UE has subscribed to those.
10583: 15.18.4	Method of test
10584: Initial conditions
10585: UE contains either ISIM and USIM applications or only USIM application on UICC. UE has activated a PDP context, discovered P-CSCF, registered to IMS services by executing the generic test procedure in Annex C.2 or C.2a (GIBA only) up to the last step and thereafter created a conference by executing the generic test procedure in Annex C.10 up to its last step.
10586: SS is configured with the shared secret key of IMS AKA algorithm, related to the IMS private user identity (IMPI) configured on the UICC card equipped into the UE. SS has performed AKAv1-MD5 authentication with the UE and accepted the registration and conference.
10587: Test procedure
10588: 1)	UE invites a user to the conference created. SS waits the UE to send to the invited user a REFER request, which refers to the conference created.
10589: 2)	SS responds to the REFER request with a valid 202 Accepted response.
10590: 3)	SS sends an initial NOTIFY to tell that the invited user is trying to join the conference.
10591: 4)	UE responds to the NOTIFY request with valid 200 OK response.
10592: 5)	SS sends the final NOTIFY to tell that the invited user has successfully joined the conference.
10593: 6)	UE responds to the NOTIFY request with a valid 200 OK response.
10594: 7)	Optional: If UE subscribed the conference event package during the generic test procedure of Annex C.10, SS sends a NOTIFY for the conference event package to the UE to notify that the user joined the conference.
10595: 8) If SS sent a NOTIFY, SS waits the UE to respond the NOTIFY with 200 OK.
10596: Expected sequence
10597: Step
10598: Direction
10599: Message
10600: Comment
10602: UE
10603: SS
10606: 1
10607: -->
10608: REFER
10609: UE sends REFER to SS referring to the conference
10610: 2
10611: <--
10612: 202 Accepted
10613: The SS responds with a 202 final response
10614: 3
10615: <--
10616: NOTIFY
10617: The SS sends initial NOTIFY for the implicit subscription created by the REFER request
10618: 4
10619: -->
10620: 200 OK
10621: The UE responds the NOTIFY with 200 OK
10622: 5
10623: <--
10624: NOTIFY
10625: The SS sends a NOTIFY related to REFER request to confirm that the invited user was able to join the conference
10626: 6
10627: -->
10628: 200 OK
10629: The UE responds the NOTIFY with 200 OK
10630: 7
10631: <--
10632: NOTIFY
10633: Optional: If the UE has subscribed the conference event package, the SS sends a NOTIFY for conference event package to inform that the invited user was able to join the conference
10634: 8
10635: -->
10636: 200 OK
10637: Optional: The UE responds the NOTIFY with 200 OK
10639: Specific Message Contents
10640: REFER (Step 1)
10641: Use the default message "MO REFER" in annex A.2.10 with the following exceptions:
10642: Header/param
10643: Value/remark
10644: Request-URI
10645: SIP URI of the user invited to the conference
10646: Refer-To
10648: 	addr-spec
10649: sip:final@conf-factory. appended with px_IMS_HomeDomainName
10650: To
10652: 	addr-spec
10653: SIP URI of the user invited to the conference
10654: 	tag	
10655: no tag given
10656: Call-ID
10658: 	callid
10659: value different to that received in INVITE message used to create the conference
10660: CSeq
10662: 	value
10663: must be present, value not checked
10665: 202 Accepted for REFER (Step 2)
10666: Use the default message "202 Accepted" in annex A.3.3.
10667: NOTIFY (Step 3)
10668: Use the default message "MT NOTIFY for refer package" in annex A.2.11 with the following exceptions:
10669: Header/param
10670: Value/remark
10671: Message-body
10672: SIP/2.0 100 Trying
10674: 200 OK for NOTIFY (Step 4)
10675: Use the default message "200 OK for other requests than REGISTER or SUBSCRIBE" in annex A.3.1.
10676: NOTIFY (Step 5)
10677: Use the default message "MT NOTIFY for refer package" in annex A.2.11 with the following exceptions:
10678: Header/param
10679: Value/remark
10680: Subscription-State
10682: 	substate-value
10683: terminated
10684: 	expires
10685: omitted from the request
10686: 	reason
10687: noresource
10688: Message-body
10689: SIP/2.0 200 OK
10691: 200 OK for NOTIFY (Step 6)
10692: Use the default message "200 OK for other requests than REGISTER or SUBSCRIBE" in annex A.3.1.
10693: NOTIFY (Step 7)
10694: Use the default message "NOTIFY for conference event package" in annex A.5.3 with the following exceptions:
10695: Header/param
10696: Value/remark
10697: Message-body
10698: <?xml version="1.0" encoding="UTF-8"?>
10699:  <conference-info   xmlns="urn:ietf:params:xml:ns:conference-info">
10700:                       entity="sip:final@conf-factory. appended with px_IMS_HomeDomainName" 
10701:                       state="partial" 
10702:                       version="1" 
10703:    <users>
10704:      <user entity=" SIP URI of the invited user">
10705:       <endpoint entity=" Contact URI of the invited user">
10706:        <status>connected</status>
10707:        <joining-method>dialed-in</joining-method>
10708:        <media id="1">
10709:         <type>audio</type>
10710:         <label>11223</label>
10711:         <src-id>random SSRC value</src-id>
10712:         <status>sendrecv</status>
10713:        </media>
10714:       </endpoint>
10715:      </users>
10716:    </conference-info>
10718: 200 OK for NOTIFY (Step 8)
10719: Use the default message "200 OK for other requests than REGISTER or SUBSCRIBE" in annex A.3.1.
10720: 15.18.5	Test requirements
10721: SS must check that the UE sends all the requests over the security associations set up during registration, in accordance to 3GPP TS 24.229 [10], clause 5.1.1.5.1.
```

## 15.19.3-15.19.5 Inviting user to conference by sending REFER to the conference focus（行 10738-10808；used_by: TC-021）

关键官方标记：`15.19.3	Test purpose`、`15.19.4	Method of test`、`Expected sequence`、`Specific Message Contents`、`15.19.5	Test requirements`、`REFER`、`NOTIFY`

```text
10738: 15.19.3	Test purpose
10739: 1)	To verify that the UE sends a correctly composed REFER request to invite a user to a conference; and
10740: 2)	To verify that the UE correctly processes the NOTIFYs from the invited user; and
10741: 3)	To verify that the UE correctly processes the NOTIFYs for the conference event package if the UE has subscribed to those.
10742: 15.19.4	Method of test
10743: Initial conditions
10744: UE contains either ISIM and USIM applications or only USIM application on UICC. UE has discovered P-CSCF, registered to IMS services by executing the generic test procedure in Annex C.2 up to the last step and thereafter created a conference by executing the generic test procedure in Annex C.10 up to its last step.
10745: SS is configured with the shared secret key of IMS AKA algorithm, related to the IMS private user identity (IMPI) configured on the UICC card equipped into the UE. SS has performed AKAv1-MD5 authentication with the UE and accepted the registration and conference.
10746: Test procedure
10747: 1)	UE invites a user to the conference created. SS waits for the UE to send to the conference focus a REFER request, which refers to the user to be invited to the conference.
10748: 2-9)	UE sends REFER to focus and receives corresponding notifications.
10749: 9A) 	UE is triggered to leave the conference.
10750: 10-11)	UE leaves conference.
10751: 12-13)	SS notifies UE about subscription end.
10752: Expected sequence
10753: Step
10754: Direction
10755: Message
10756: Comment
10758: UE
10759: SS
10762: 1
10764: Make the UE invite another user to the conference
10765: UE sends REFER to SS referring to the conference
10766: 2-9
10768: Steps defined in annex C.19
10770: 9A
10773: Make UE leave the conference
10774: 10
10775: -->
10776: BYE
10777: The UE leaves the conference with BYE
10778: 11
10779: <--
10780: 200 OK
10781: The SS sends 200 OK for BYE
10782: 12
10783: <--
10784: NOTIFY
10785: If the UE had subscribed to the conference event package, the SS notifies the UE that its subscription to conference event package is terminated
10786: 13
10787: -->
10788: 200 OK
10789: The UE sends 200 OK for NOTIFY (if sent by SS)
10791: Specific Message Contents
10792: BYE (Step 10)
10793: Use the default message "BYE" in annex A.2.8 but with the following exceptions:
10794: Header/param
10795: Value/remark
10796: Request-Line
10798: 	Request-URI
10799: sip:final@conf-factory. appended with px_IMS_HomeDomainName
10801: 200 OK for BYE (Step 11)
10802: Use the default message "200 OK for other requests than REGISTER or SUBSCRIBE" in annex A.3.1.
10803: NOTIFY (Step 12)
10804: Use the default message "NOTIFY for conference event package" in annex A.5.3 with condition A4.
10805: 200 OK for NOTIFY (Step 13)
10806: Use the default message "200 OK for other requests than REGISTER or SUBSCRIBE" in annex A.3.1.
10807: 15.19.5	Test requirements
10808: SS must check that the UE sends all the requests over the security associations set up during registration, in accordance to 3GPP TS 24.229 [10], clause 5.1.1.5.1.
```

## 15.21.3-15.21.5 Joining a conference after being invited to it（行 10925-11364；used_by: TC-021）

关键官方标记：`15.21.3	Test purpose`、`15.21.4	Method of test`、`Expected sequence`、`Specific Message Contents`、`15.21.5	Test requirements`、`PRACK`、`UPDATE`、`NOTIFY`

```text
10925: 15.21.3	Test purpose
10926: 1)	To verify that the UE correctly processes the REFER request which invites the user to join the conference; and
10927: 2)	To verify that the UE issues correctly composed NOTIFYs to report its progress; and
10928: 3)	To verify that the UE sets up a new dialog with conference focus by sending an INVITE request; and
10929: 4)	To verify that the UE terminates the dialog with the conference focus when receiving a BYE request.
10930: 15.21.4	Method of test
10931: Initial conditions
10932: UE contains either ISIM and USIM applications or only USIM application on UICC. UE has discovered P-CSCF and registered to IMS services, by executing the generic test procedure in Annex C.2 or C.2a (GIBA only) up to the last step.
10933: SS is configured with the shared secret key of IMS AKA algorithm, related to the IMS private user identity (IMPI) configured on the UICC card equipped into the UE. SS has performed AKAv1-MD5 authentication with the UE and accepted the registration.
10934: Test procedure applicable for a UE with E-UTRA support (TS 34.229-2 [5] A.18/1)
10935: 0)	SS pages the UE to perform procedure described in TS 36.508 [94] table 4.5A.7.3-1 steps 1-8
10936: 1)	SS sends to the UE a REFER request, which refers to the conference focus.
10937: 2)	SS waits the UE to respond to the REFER request with a valid 202 Accepted response.
10938: 3)	SS waits the UE to send an INVITE request to the conference focus
10939: 4)	SS responds to the INVITE request with a 100 Trying response
10940: 5)	SS waits the UE to send an initial NOTIFY to tell that it is trying to join the conference.
10941: 6)	SS responds to the NOTIFY request with valid 200 OK response.
10942: 7)	SS responds to the INVITE request with a 183 Session in Progress response 
10943: 7a)	SS starts activation of dedicated EPS bearer according to TS 36.508 [94] table 4.5A.7.3-1 steps 13-15
10944: 8)	SS waits for the UE to send a PRACK request possibly containing the second SDP offer.
10945: 9)	SS responds to the PRACK request with valid 200 OK response.
10946: 10)	SS waits for the UE to optionally send a UPDATE request containing the final SDP offer. UE will not send the UPDATE request if the PRACK in step 8 already contained the final offer with preconditions met.
10947: 11)	SS responds to the UPDATE request (if UE sent one) with valid 200 OK response.
10948: 12)	SS responds to the INVITE request with a 200 OK response
10949: 13)	SS waits the UE to send an ACK and NOTIFY requests. Additionally the UE may send a SUBCRIBE request for the conference event package. The UE is allowed to send these requests in any order.
10950: 14)	SS responds to the NOTIFY request with a valid 200 OK response.
10951: 15)	If UE sent SUBSCRIBE, SS responds to it with 200 OK response.
10952: 16)	If UE sent SUBSCRIBE, SS sends a NOTIFY for the conference event package to the UE.
10953: 17)	If SS sent a NOTIFY, SS waits the UE to respond the NOTIFY with 200 OK.
10954: 18)	SS sends a BYE request in order to remove the UE from the conference
10955: 19)	SS waits the UE to respond to the BYE request with a valid 200 OK response.
10956: 20)	SS notifies the UE that its subscription to conf event is terminated.
10957: 21)	UE responds with 200 OK.
10958: Expected sequence
10959: Step
10960: Direction
10961: Message
10962: Comment
10964: UE
10965: SS
10968: 0
10971: Radio Bearer Establishment according to TS 36.508 [94] table 4.5A.7.3-1 (steps 1 to 8)
10972: 1
10973: <--
10974: REFER
10975: SS sends REFER to UE referring to the conference
10976: 2
10977: -->
10978: 202 Accepted
10979: UE responds with a 202 Accepted response
10980: 3
10981: -->
10982: INVITE
10983: UE sends INVITE to set up a dialog with conference focus. UE indicates the medias and codecs the UE supports. 
10984: 4
10985: <--
10986: 100 Trying
10987: SS responds the INVITE with 100 Trying
10988: 5
10989: -->
10990: NOTIFY
10991: UE sends initial NOTIFY for the implicit subscription created by the REFER request
10992: 6
10993: <--
10994: 200 OK
10995: SS responds the NOTIFY with 200 OK
10996: 7
10997: <--
10998: 183 Session in Progress
10999: SS responds with an SDP answer only supporting AMR audio codec 
11000: 7a
11003: Activation of dedicated EPS bearer according to TS 36.508 [94] table 4.5A.7.3-1 steps 13-15
11004: NOTE: Activation is started by the SS but messages sent by the UE are in parallel to step 8
11005: 8
11006: -->
11007: PRACK
11008: UE acknowledges the receipt of 183 response with PRACK and optionally offers second SDP that indicates preconditions as met 
11009: 9
11010: <--
11011: 200 OK
11012: The SS responds PRACK with 200 OK and answers the second SDP with mirroring its contents and indicates having reserved the resources if UE has also done so.
11013: 10
11014: -->
11015: UPDATE
11016: Optional step: UE sends an UPDATE after having reserved the resources with GPRS procedures for PDP context used for the media
11017: 11
11018: <--
11019: 200 OK
11020: Optional step: The SS responds UPDATE with 200 OK and indicates having reserved the resources 
11021: 12
11022: <--
11023: 200 OK
11024: SS responds the INVITE with 200 OK
11025: 13
11026: -->
11027: ACK
11028: NOTIFY
11029: SUBSCRIBE (optional message)
11030: UE sends the ACK to complete three-way handshake for INVITE and NOTIFY to confirm that the UE was able to join the conference. Additionally the UE may subscribe to the conference event package related to the conference to which the user joined. 
11031: Note that the UE may send these messages in any order; the SS shall wait up to 3s for the UE to send the optional SUBSCRIBE
11032: 14
11033: <--
11034: 200 OK
11035: SS responds the NOTIFY with 200 OK
11036: 15
11037: <--
11038: 200 OK
11039: Optional step: SS responds to the subscription if the UE sent the SUBSCRIBE request
11040: 16
11041: <--
11042: NOTIFY
11043: Optional step: SS sends the initial state of the conference event to the UE if the UE subscribed it
11044: 17
11045: -->
11046: 200 OK
11047: Optional step: UE responds to the NOTIFY
11048: 18
11049: <--
11050: BYE
11051: SS sends a BYE to remove the UE from the conference
11052: 19
11053: -->
11054: 200 OK
11055: UE responds the BYE with 200 OK
11056: 20
11057: <--
11058: NOTIFY
11059: If the UE had subscribed to the conference event package, the SS notifies the UE that its subscription to conference event package is terminated
11060: 21
11061: -->
11062: 200 OK
11063: The UE sends 200 OK for NOTIFY (if sent by SS)
11065: In addition to the steps shown above the UE might send extra NOTIFY requests to indicate the progress e.g. after receiving the 183 response from the SS. As the timing of these optional NOTIFY requests from the UE is not deterministic, they are not shown in the expected sequence. SS must be prepared to receive such NOTIFY requests between steps 3 and 13 and respond to them with 200 OK response.
11066: Specific Message Contents
11067: REFER (Step 1)
11068: Use the default message "MT REFER" in annex A.2.12 with the following exceptions:
11069: Header/param
11070: Value/remark
11071: Request-URI
11072: Contact URI of the UE invited to the conference (as within the REGISTER request from the UE)
11073: Refer-To
11075: 	addr-spec
11076: sip:final@conf-factory. appended with px_IMS_HomeDomainName
11077: Referred-by
11078: -- check this
11079: 	addr-spec
11080: sip:master@conference.com
11081: To
11083: 	addr-spec
11084: SIP URI of the user invited to the conference
11085: 	tag	
11086: no tag given
11087: Call-ID
11089: 	callid
11090: any value according to Call-ID syntax can be used
11091: CSeq
11093: 	value
11094: any value according to CSeq syntax can be used
11096: 202 Accepted for REFER (Step 2)
11097: Use the default message "202 Accepted" in annex A.3.3.
11098: INVITE (Step 3)
11099: Use the default message "INVITE for MO call setup" in annex A.2.1 with the following exceptions:
11100: Header/param
11101: Value/remark
11102: Request-Line
11104: 	Request-URI
11105: sip:final@conf-factory. appended with px_IMS_HomeDomainName
11106: To
11108: 	addr-spec
11109: sip:final@conf-factory. appended with px_IMS_HomeDomainName
11110: Referred-by
11112: 	addr-spec
11113: sip:master@conference.com
11114: Supported
11116: 	option-tag
11117: precondition
11118: Message-body
11119: The following SDP types and values.
11121: Session description:
11122: -	v=0
11123: -	o=(username) (sess-id) (sess-version) IN (addrtype) (unicast-address for UE)
11124: -	s=(session name)
11125: -	c=IN (addrtype) (connection-address for UE) [Note 1]
11126: -	b=AS: (bandwidth-value)
11128: Time description:
11129: -	t= (start-time) (stop-time)
11131: Media description:
11132: -	m=audio (transport port) RTP/AVP (fmt)
11133: -	c=IN (addrtype) (connection-address for UE) [Note 1]
11134: -	b=AS: (bandwidth-value)
11135: -	b=RS: (bandwidth-value)
11136: -	b=RR: (bandwidth-value)
11138: Attributes for media:
11139: -	a=rtpmap: (payload type) AMR-WB/16000 [Note 2]
11140: -	a=fmtp: (format) mode-change-capability=2; max-red=(att-field) [Note 3]
11141: -	a=rtpmap: (payload type) telephone-event/16000
11142: -	a=fmtp: (format)
11143: -	a=ptime:20
11144: -	a=maxptime:240
11146: Attributes for preconditions:
11147: -	a=curr:qos local none
11148: -	a=curr:qos remote none
11149: -	a=des:qos mandatory local sendrecv
11150: -	a=des:qos optional remote sendrecv
11152: Note 1: At least one "c=" field shall be present.
11153: Note 2: The AMR channel number shall be "/1" or omitted.
11154: Note 3: Values from 0 to 220 are allowed
11156: 100 Trying for INVITE (Step 4)
11157: Use the default message "100 Trying for INVITE" in annex A.2.2.
11158: NOTIFY (Step 5)
11159: Use the default message "MO NOTIFY for refer package" in annex A.2.13 with the following exceptions:
11160: Header/param
11161: Value/remark
11162: Message-body
11163: SIP/2.0 100 Trying
11165: 200 OK for NOTIFY (Step 6)
11166: Use the default message "200 OK for other requests than REGISTER or SUBSCRIBE" in annex A.3.1.
11167: 183 Session in Progress for INVITE (Step 7)
11168: Use the default message "183 Session in Progress for INVITE" in annex A.2.3 with the following exceptions:
11169: Header/param
11170: Value/remark
11171: Require
11173: 	option-tag	
11174: precondition
11175: Contact
11177: 	addr-spec
11178: sip:final@conf-factory. appended with px_IMS_HomeDomainName
11179: Message-body
11180: The following SDP types and values.
11182: Session description:
11183: -	v=0
11184: -	o=1111111111 1111111111 IN (addrtype) (unicast-address for SS)
11185: -	s=-
11186: -	c=IN (addrtype) (connection-address for SS)
11187: -	b=AS:37
11189: Time description:
11190: -	t=0 0
11192: Media description:
11193: -	m=audio (transport port) RTP/AVP (fmt) [Note 1]
11194: -	b=AS: (bandwidth-value) [Note 1]
11195: -	b=RS: (bandwidth-value) [Note 1]
11196: -	b=RR: (bandwidth-value) [Note 1]
11198: Attributes for media:
11199: -	a=rtpmap: (payload type) AMR-WB/16000/1 [Note 1]
11201: -	a=fmtp: (format) mode-change-capability=2; max-red=220 [Note 1]
11202: -	a=ptime:20
11203: -	a=maxptime:240
11204: -	a=inactive [Note 2]
11206: Attributes for preconditions:
11207: -	a=curr:qos local none
11208: -	a=curr:qos remote none
11209: -	a=des:qos mandatory local sendrecv
11210: -	a=des:qos mandatory remote sendrecv
11211: -	a=conf:qos remote sendrecv
11213: Note 1: The value for fmt, bandwidth, payload type and format copied from step 3.
11214: Note 2: The attribute a=inactive shall be present if it was included in step 3.
11216: PRACK (Step 8)
11217: Use the default message "PRACK" in annex A.2.4 with the exception that either Supported or Require header shall contain the "precondition" tag and with the following exceptions:
11218: Header/param
11219: Value/remark
11220: Content-Type
11221: header shall be present only if there is SDP in message-body
11222: 	media-type
11223: application/sdp
11224: Content-Length
11225: header shall be present if UE uses TCP to send this request and if there is a message-body
11226: 	value
11227: length of message-body
11228: Message-body
11229: Header optional
11231: Contents if present: The following SDP types and values shall be present.
11233: Session description:
11234: -	v=0
11235: -	o=(username) (sess-id) (sess-version) IN (addrtype) (unicast-address for UE) [Note 2]
11236: -	s=(session name)
11237: -	c=IN (addrtype) (connection-address for UE) [Note 1]
11238: -	b=AS: (bandwidth-value)
11240: Time description:
11241: -	t=0 0
11243: Media description:
11244: -	m=audio (transport port) RTP/AVP (fmt)
11245: -	c=IN (addrtype) (connection-address for UE) [Note 1]
11246: -	b=AS: (bandwidth-value)
11247: -	b=RS: (bandwidth-value)
11248: -	b=RR: (bandwidth-value)
11250: Attributes for media:
11251: -	a=rtpmap: (payload type) AMR-WB/16000 [Note 3]
11252: -	a=fmtp: (format)
11253: -	a=sendrecv
11255: Attributes for preconditions:
11256: -	a=curr:qos local sendrecv
11257: -	a=curr:qos remote none
11258: -	a=des:qos mandatory local sendrecv
11259: -	a=des:qos optional remote sendrecv or a=des:qos mandatory remote sendrecv
11261: Note 1: At least one "c=" field shall be present.
11262: Note 2: "o=" line identical to previous SDP sent by UE except that sess-version is incremented by one
11263: Note 3: The AMR channel number shall be "/1" or omitted.
11264: 200 OK for PRACK (Step 9)
11265: Use the default message "200 OK for other requests than REGISTER or SUBSCRIBE" in annex A.3.1 with the following exceptions:
11266: Header/param
11267: Value/remark
11268: Content-Type
11269: header shall be present only if there is SDP in message-body
11270: 	media-type
11271: application/sdp
11272: Content-Length
11274: 	value
11275: length of message-body
11276: Message-body
11277: Header present if Prack (step 8) contained SDP.
11278: Contents if present: SDP body of the 200 response copied from the received PRACK and modified as follows:
11279: -	"o=" line identical to previous SDP sent by SS except that sess-version is incremented by one
11280: -	IP address on "c=" lines and transport port on "m=" lines changed to indicate to which IP address and port the UE should start sending the media;
11281: Attributes for preconditions:
11282: a=curr:qos remote sendrecv 
11285: UPDATE (Step 10) optional step used when PRACK contained a=curr:qos local none
11286: Use the default message "UPDATE" in annex A.2.5 with the exception that either Supported or Require header shall contain the "precondition" tag and with the following exceptions:
11287: Header/param
11288: Value/remark
11289: Message-body
11290: Same contents as specified in step 8.
11291: 200 OK for UPDATE (Step 11) - optional step used when UE sent UPDATE
11292: Use the default message "200 OK for other requests than REGISTER or SUBSCRIBE" in annex A.3.1 with the following exceptions:
11293: Header/param
11294: Value/remark
11295: Content-Type
11297: 	media-type
11298: application/sdp
11299: Content-Length
11301: 	value
11302: length of message-body
11303: Message-body
11304: SDP body of the 200 response copied from the received UPDATE but modified as follows:
11306: "o=" line identical to previous SDP sent by SS except that sess-version is incremented by one
11308: -	IP address on "c=" line and transport port on "m=" lines changed to indicate to which IP address and port the UE should start sending the media; and
11310: -	the "a=" lines describing the current and desired state of the preconditions, as described in RFC 3312 [31], updated as follows:
11311: a=curr:qos local sendrecv
11312: a=curr:qos remote sendrecv
11313: a=des:qos mandatory local sendrecv
11314: a=des:qos mandatory remote sendrecv
11316: 200 OK for INVITE (Step 12)
11317: Use the default message "200 OK for other requests than REGISTER or SUBSCRIBE" in annex A.3.1 with the following exceptions:
11318: Header/param
11319: Value/remark
11320: Contact
11322: 	addr-spec
11323: sip:final@conf-factory. appended with px_IMS_HomeDomainName
11325: ACK (Step 13)
11326: Use the default message "ACK" in annex A.2.7.
11327: NOTIFY (Step 13)
11328: Use the default message "MO NOTIFY for refer package" in annex A.2.13 with the following exceptions:
11329: Header/param
11330: Value/remark
11331: Subscription-State
11333: 	substate-value
11334: terminated
11335: 	expires
11336: omitted from the request
11337: 	reason
11338: noresource
11339: Message-body
11340: SIP/2.0 200 OK
11342: SUBSCRIBE (Step 13)
11343: Use the default message "SUBSCRIBE for conference event package" in annex A.5.1.
11344: 200 OK for NOTIFY (Step 14)
11345: Use the default message "200 OK for other requests than REGISTER or SUBSCRIBE" in annex A.3.1.
11346: 200 OK for SUBSCRIBE (Step 15)
11347: Use the default message "200 OK for SUBSCRIBE" in annex A.5.2.
11348: NOTIFY (Step 16)
11349: Use the default message "NOTIFY for conference event package" in annex A.5.3 with condition A3. 
11350: 200 OK for NOTIFY (Step 17)
11351: Use the default message "200 OK for other requests than REGISTER or SUBSCRIBE" in annex A.3.1.
11352: BYE (Step 18)
11353: Use the default message "BYE" in annex A.2.8. 
11354: 200 OK for BYE (Step 19)
11355: Use the default message "200 OK for other requests than REGISTER or SUBSCRIBE" in annex A.3.1
11356: NOTIFY (Step 20)
11357: Use the default message "NOTIFY for conference event package" in annex A.5.3 with condition A4.
11358: 200 OK for NOTIFY (Step 21)
11359: Use the default message "200 OK for other requests than REGISTER or SUBSCRIBE" in annex A.3.1.
11360: 15.21.5	Test requirements
11361: SS must check that the UE sends all the requests over the security associations set up during registration, in accordance to 3GPP TS 24.229 [10], clause 5.1.1.5.1.
11362: Step 3: the UE shall send an INVITE message with correct content according to the Specific Message Contents above.
11363: Step 8: the UE shall send a PRACK request with the correct content according to the Specific Message Contents above. 
11364: Step 10: the UE may conditionally send an UPDATE request with the correct content according to the Specific Message Contents above. 
```

> 状态：这些块是调用类 TC 的官方 TP 骨架来源；正式 P/F 仍只能由 SS/一致性仪表按对应条目执行产生。

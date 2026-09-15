# TC-011/013/014/015/032 官方 TP 过程原文（34.229-1）

来源：`3GPP TS 34.229-1` V14.7.0 (2019-06)，逐行抽取自 `C:\Users\co1750\Documents\Codex\2026-09-02\i\_extract\34229-1e70-word.txt`；行号口径 `Python str.splitlines()` 1-based。

每个块覆盖完整官方用例正文（Definition 至 Test requirements），只固化原文，不把本地执行结果升级为官方一致性 PASS。

## 8.1 Initial registration（行 3875-4151；used_by: TC-011）

关键官方标记：`8.1.1	Definition`、`8.1.2	Conformance requirement`、`8.1.3	Test purpose`、`8.1.4	Method of test`、`8.1.5	Test requirements`、`AKAv1-MD5`、`Security-Client`、`Security-Server`、`reg event package`

```text
3875: 8.1	Initial registration 
3876: 8.1.1	Definition
3877: Test to verify that the UE can correctly register to IMS services when equipped with UICC that contains either both ISIM and USIM applications or only USIM application but not ISIM. The process consists of sending initial registration to S-CSCF via the P-CSCF discovered, authenticating the user and finally subscribing the registration event package for the registered default public user identity. 
3878: 8.1.2	Conformance requirement
3879: [TS 24.229, clause C.2]:
3880: In case the UE is loaded with a UICC that contains a USIM but does not contain an ISIM, the UE shall:
3881: -	generate a private user identity;
3882: -	generate a temporary public user identity; and
3883: -	generate a home network domain name to address the SIP REGISTER request to.
3884: All these three parameters are derived from the IMSI parameter in the USIM, according to the procedures described in 3GPP TS 23.003. Also in this case, the UE shall derive new values every time the UICC is changed, and shall discard existing values if the UICC is removed.
3885: NOTE:	If there is an ISIM and a USIM on a UICC, the ISIM is used for authentication to the IM CN subsystem, as described in 3GPP TS 33.203. See also subclause 5.1.1.1A.
3886: [TS 24.229, clause 5.1.1.1A]:
3887: This subclause applies when a UE contains either an ISIM or a USIM.
3888: The ISIM shall always be used for authentication to the IM CN subsystem, if it is present, as described in 3GPP TS 33.203.
3889: The ISIM is preconfigured with all the necessary parameters to initiate the registration to the IM CN subsystem. These parameters include:
3890: -	the private user identity;
3891: -	one or more public user identities; and
3892: -	the home network domain name used to address the SIP REGISTER request
3893: The first public user identity in the list stored in the ISIM is used in emergency registration requests. 
3894: In case the UE does not contain an ISIM, the UE shall:
3895: -	generate a private user identity;
3896: -	generate a temporary public user identity; and
3897: -	generate a home network domain name to address the SIP REGISTER request to;
3898: in accordance with the procedures in clause C.2.
3899: The temporary public user identity is only used in REGISTER requests, i.e. initial registration, re-registration, mobile-initiated deregistration.
3900: The UE shall not reveal to the user the temporary public user identity if the temporary public user identity is barred. The temporary public user identity is not barred if received by the UE in the P-Associated-URI header.
3901: If the UE is unable to derive the parameters in this subclause for any reason, then the UE shall not proceed with the request associated with the use of these parameters and will not be able to register to the IM CN subsystem.
3902: [TS 24.229, clause 5.1.1.2.1]:
3903: The initial registration procedure consists of the UE sending an unprotected REGISTER request and, if challenged depending on the security mechanism supported for this UE, sending the integrity-protected REGISTER request or other appropriate response to the challenge. The UE can register a public user identity with any of its contact addresses at any time after it has acquired an IP address, discovered a P-CSCF, and established an IP-CAN bearer that can be used for SIP signalling. However, the UE shall only initiate a new registration procedure when it has received a final response from the registrar for the ongoing registration, or the previous REGISTER request has timed out.
3904: When registering any public user identity belonging to the UE, the UE shall either use an already active pair of security associations or a TLS session to protect the REGISTER requests, or register the public user identity via a new initial registration procedure.
3905: When binding any one of its public user identities to an additional contact address via a new initial registration procedure, the UE shall follow the procedures described in RFC 5626. The set of security associations or a TLS session resulting from this initial registration procedure will have no impact on the existing set of security associations or TLS sessions that have been established as a result of previous initial registration procedures. However, if the UE registers any one of its public user identities with a new contact address via a new initial registration procedure and does not employ the procedures described in RFC 5626, then the new set of security associations or TLS session shall replace any existing set of security association or TLS session.
3906: If the UE detects that the existing security associations or TLS sessions associated with a given contact address are no longer active (e.g., after receiving no response to several protected messages), the UE shall: 
3907: -	consider all previously registered public user identities bound to this security associations or TLS session that are only associated with this contact address as deregistered; and
3908: -	stop processing all associated ongoing dialogs and transactions that were using the security associations or TLS session associated with this contact address, if any (i.e. no further SIP signalling will be sent by the UE on behalf of these transactions or dialogs).
3909: The UE shall send the unprotected REGISTER requests to the port advertised to the UE during the P-CSCF discovery procedure. If the UE does not receive any specific port information during the P-CSCF discovery procedure, or if the UE was pre-configured with the P-CSCF's IP address or domain name and was unable to obtain specific port information, the UE shall send the unprotected REGISTER request to the SIP default port values as specified in RFC 3261. 
3910: NOTE 1:	The UE will only send further registration and subsequent SIP messages towards the same port of the P-CSCF for security mechanisms that do not require using negotiated ports for exchanging protected messages.
3911: The UE shall extract or derive a public user identity, the private user identity, and the domain name to be used in the Request-URI in the registration, according to the procedures described in subclause 5.1.1.1A or subclause 5.1.1.1B. A public user identity may be input by the end user.
3912: [TS 24.229 Rel-8, clause 5.1.1.2.1]:
3913: On sending an unprotected REGISTER request, the UE shall populate the header fields as follows:
3914: a)	a From header field set to the SIP URI that contains the public user identity to be registered;
3915: b)	a To header field set to the SIP URI that contains the public user identity to be registered;
3916: c)	a Contact header field set to include SIP URI(s) containing the IP address or FQDN of the UE in the hostport parameter. If the UE supports GRUU (see table A.4, item A.4/53) or multiple registrations, the UE shall include a "+sip.instance" header field parameter containing the instance ID. If the UE supports multiple registrations it shall include "reg-id" header field parameter as described in RFC 5626. The UE shall include all supported ICSI values (coded as specified in subclause 7.2A.8.2) in a g.3gpp.icsi-ref media feature tag as defined in subclause 7.9.2 and RFC 3840 for the IMS communication services it intends to use, and IARI values (coded as specified in subclause 7.2A.9.2), for the IMS applications it intends to use in a g.3gpp.iari-ref media feature tag as defined in subclause 7.9.3 and RFC 3840;
3917: d)	a Via header field set to include the sent-by field containing the IP address or FQDN of the UE and the port number where the UE expects to receive the response to this request when UDPis used. For TCP, the response is received on the TCP connection on which the request was sent. The UE shall also include a "rport" header field parameter with no value in the Via header field. Unless the UE has been configured to not send keep-alives, and unless the UE is directly connected to an IP-CAN for which usage of NAT is not defined, it shall include a "keep" header field parameter with no value in the Via header field, in order to indicate support of sending keep-alives associated with the registration, as described in RFC 6223;
3918: NOTE 2:	When sending the unprotected REGISTER request using UDP, the UE transmit the request from the same IP address and port on which it expects to receive the response to this request.
3919: e)	a registration expiration interval value of 600 000 seconds as the value desired for the duration of the registration;
3920: NOTE 3:	The registrar (S-CSCF) might decrease the duration of the registration in accordance with network policy. Registration attempts with a registration period of less than a predefined minimum value defined in the registrar will be rejected with a 423 (Interval Too Brief) response.
3921: f)	a Request-URI set to the SIP URI of the domain name of the home network used to address the REGISTER request;
3922: g)	the Supported header field containing the option-tag "path", and
3923: 1)	if GRUU is supported, the option-tag "gruu"; and
3924: 2)	if multiple registrations is supported, the option-tag "outbound".
3925: h)	if a security association or TLS session exists, and if available to the UE (as defined in the access technology specific annexes for each access technology), a P-Access-Network-Info header field set as specified for the access network technology (see subclause 7.2A.4).
3926: [TS 24.229 Rel-9, clause 5.1.1.2.1]:
3927: ...
3928: h)	if a security association or TLS session exists, and if available to the UE (as defined in the access technology specific annexes for each access technology), a P-Access-Network-Info header field set as specified for the access network technology (see subclause 7.2A.4); and
3929: i)	a Security-Client header field to announce the media plane security mechanisms the UE supports, if any, labelled with the "mediasec" header field parameter specified in subclause 7.2A.7.
3930: NOTE 4:	The "mediasec" header field parameter indicates that security mechanisms are specific to the media plane.
3931: [TS 24.229 Rel-8, clause 5.1.1.2.1]:
3932: On receiving the 200 (OK) response to the REGISTER request, the UE shall:
3933: a)	store the expiration time of the registration for the public user identities found in the To header field value and bind it either to the respective contact address of the UE or to the registration flow and the associated contact address (if the multiple registration mechanism is used);
3934: b)	store as the default public user identity the first URI on the list of URIs present in the P-Associated-URI header field and bind it to the respective contact address of the UE and the associated set of security associations or TLS session;
3935: NOTE 4:	When using the respective contact address and associated set of security associations or TLS session, the UE can utilize additional URIs contained in the P-Associated-URI header field and bound it to the respective contact address of the UE and the associated set of security associations or TLS session, e.g. for application purposes.
3936: c)	treat the identity under registration as a barred public user identity, if it is not included in the P-Associated-URI header field;
3937: d)	store the list of service route values contained in the Service-Route header field and bind the list either to the contact address or to the registration flow and the associated set of security associations or TLS session over which the REGISTER request was sent; 
3938: NOTE 5:	When multiple registration mechanism is not used, there will be only one list of service route values bound to a contact address. However, when multiple registration mechanism is used, there will be different list of service route values bound to each registration flow and the associated contact address.
3939: NOTE 6:	The UE will use the stored list of service route values to build a proper preloaded Route header field for new dialogs and standalone transactions when using either the respective contact address or to the registration flow and the associated contact address (if the multiple registration mechanism is used), and the associated set of security associations or TLS session.
3940: e)	find the Contact header field within the response that matches the one included in the REGISTER request. If this contains a "pub-gruu" header field parameter or a "temp-gruu" header field parameter or both, and the UE supports GRUU (see table A.4, item A.4/53), then store the value of those parameters as the GRUUs for the UE in association with the public user identity and the contact address that was registered;
3941: f)	if the REGISTER request contained the "reg-id" and "+sip.instance" Contact header field parameter and the "outbound" option tag in a Supported header field, the UE shall check whether the option-tag "outbound" is present in the Require header field:
3942: -	if no option-tag "outbound" is present, the UE shall conclude that the S-CSCF does not support the registration procedure as described in RFC 5626, and the S-CSCF has followed the registration procedure as described in RFC 5627 or RFC 3261, i.e., if there is a previously registered contact address, the S-CSCF replaced the old contact address and associated information with the new contact address and associated information (see bullet e) above). Upon detecting that the S-CSCF does not support the registration procedure as defined in RFC 5626, the UE shall refrain from registering any additional IMS flows for the same private identity as described in RFC 5626; or
3943: NOTE 7:	Upon replaces the old contact address with the new contact address, the S-CSCF performs the network initiated deregistration procedure for the previously registered public user identities and the associated old contact address as described in subclause 5.4.1.5. Hence, the UE will receive a NOTIFY request informing the UE about the deregistration of the old contact address. 
3944: -	if an option-tag "outbound" is present, the UE may establish additional IMS flows for the same private identity, as defined in RFC 5626; and
3945: g)	if the Via header field contains a "keep" header field parameter with a value, unless the UE detects that it is not behind a NAT, start to send keep-alives associated with the registration towards the P-CSCF, as described in RFC 6223.[TS 24.229 Rel-9, clause 5.1.1.2.1]:
3946: ...
3947: g)	store the announcement of media plane security mechanisms the P-CSCF (IMS-ALG) supports labelled with the "mediasec" header field parameter specified in subclause 7.2A.7 and received in the Security-Server header field, if any. Once the UE chooses a media security mechanism from the list received in the Security-Server header field from the server, it may initiate that mechanism on a media level when it initiates new media in an existing session; and
3948: NOTE 9:	The "mediasec" header field parameter indicates that security mechanisms are specific to the media plane
3949: h)	if the Via header field contains a "keep" header field parameter with a value, unless the UE detects that it is not behind a NAT, start to send keep-alives associated with the registration towards the P-CSCF, as described in RFC 6223.
3950: [TS 24.229 Rel-10, clause 5.1.1.2.1]:
3951: On sending an unprotected REGISTER request, the UE shall populate the header fields as follows:
3952: a)	a From header field set to the SIP URI that contains the public user identity to be registered;
3953: b)	a To header field set to the SIP URI that contains the public user identity to be registered;
3954: c)	a Contact header field set to include SIP URI(s) containing the IP address or FQDN of the UE in the hostport parameter. If the UE:
3955: 1)	supports GRUU (see table A.4, item A.4/53);
3956: 2)	supports multiple registrations;
3957: 3)	has an IMEI available; or
3958: 4)	has an MEID available;
3959: 	the UE shall include a "+sip.instance" header field parameter containing the instance ID. Only the IMEI shall be used for generating an instance ID for a multi-mode UE that supports both 3GPP and 3GPP2 defined radio access networks.
3960: NOTE 2:	The requirement placed on the UE to include an instance ID based on the IMEI or the MEID when the UE does not support GRUU and does not support multiple registrations does not imply any additional requirements on the network.
3961: 	If the UE supports multiple registrations it shall include "reg-id" header field parameter as described in RFC 5626 [92]. The UE shall include all supported ICSI values (coded as specified in subclause 7.2A.8.2) in a g.3gpp.icsi-ref media feature tag as defined in subclause 7.9.2 and RFC 3840 [62] for the IMS communication services it intends to use, and IARI values (coded as specified in subclause 7.2A.9.2), for the IMS applications it intends to use in a g.3gpp.iari-ref media feature tag as defined in subclause 7.9.3 and RFC 3840 [62];
3962: d)	a Via header field set to include the sent-by field containing the IP address or FQDN of the UE and the port number where the UE expects to receive the response to this request when UDPis used. For TCP, the response is received on the TCP connection on which the request was sent. The UE shall also include a "rport" header field parameter with no value in the Via header field. Unless the UE has been configured to not send keep-alives, and unless the UE is directly connected to an IP-CAN for which usage of NAT is not defined, it shall include a "keep" header field parameter with no value in the Via header field, in order to indicate support of sending keep-alives associated with the registration, as described in RFC 6223 [143];
3963: NOTE 3:	When sending the unprotected REGISTER request using UDP, the UE transmit the request from the same IP address and port on which it expects to receive the response to this request.
3964: e)	a registration expiration interval value of 600 000 seconds as the value desired for the duration of the registration;
3965: NOTE 4:	The registrar (S-CSCF) might decrease the duration of the registration in accordance with network policy. Registration attempts with a registration period of less than a predefined minimum value defined in the registrar will be rejected with a 423 (Interval Too Brief) response.
3966: f)	a Request-URI set to the SIP URI of the domain name of the home network used to address the REGISTER request;
3967: g)	the Supported header field containing the option-tag "path", and
3968: 1)	if GRUU is supported, the option-tag "gruu"; and
3969: 2)	if multiple registrations is supported, the option-tag "outbound".
3970: h)	if a security association or TLS session exists, and if available to the UE (as defined in the access technology specific annexes for each access technology), a P-Access-Network-Info header field set as specified for the access network technology (see subclause 7.2A.4); and
3971: i)	a Security-Client header field to announce the media plane security mechanisms the UE supports, if any, labelled with the "mediasec" header field parameter specified in subclause 7.2A.7.
3972: NOTE 5:	The "mediasec" header field parameter indicates that security mechanisms are specific to the media plane.
3973: On receiving the 200 (OK) response to the REGISTER request, the UE shall:
3974: a)	store the expiration time of the registration for the public user identities found in the To header field value and bind it either to the respective contact address of the UE or to the registration flow and the associated contact address (if the multiple registration mechanism is used);
3975: b)	store as the default public user identity the first URI on the list of URIs present in the P-Associated-URI header field and bind it to the respective contact address of the UE and the associated set of security associations or TLS session;
3976: NOTE 6:	When using the respective contact address and associated set of security associations or TLS session, the UE can utilize additional URIs contained in the P-Associated-URI header field and bound it to the respective contact address of the UE and the associated set of security associations or TLS session, e.g. for application purposes.
3977: c)	treat the identity under registration as a barred public user identity, if it is not included in the P-Associated-URI header field;
3978: d)	store the list of service route values contained in the Service-Route header field and bind the list either to the contact address or to the registration flow and the associated contact address (if the multiple registration mechanism is used), and the associated set of security associations or TLS session over which the REGISTER request was sent;
3979: NOTE 7:	When multiple registration mechanism is not used, there will be only one list of service route values bound to a contact address. However, when multiple registration mechanism is used, there will be different list of service route values bound to each registration flow and the associated contact address.
3980: NOTE 8:	The UE will use the stored list of service route values to build a proper preloaded Route header field for new dialogs and standalone transactions when using either the respective contact address or to the registration flow and the associated contact address (if the multiple registration mechanism is used), and the associated set of security associations or TLS session.
3981: e)	find the Contact header field within the response that matches the one included in the REGISTER request. If this contains a "pub-gruu" header field parameter or a "temp-gruu" header field parameter or both, and the UE supports GRUU (see table A.4, item A.4/53), then store the value of those parameters as the GRUUs for the UE in association with the public user identity and the contact address that was registered;
3982: f)	if the REGISTER request contained the "reg-id" and "+sip.instance" Contact header field parameter and the "outbound" option tag in a Supported header field, the UE shall check whether the option-tag "outbound" is present in the Require header field:
3983: -	if no option-tag "outbound" is present, the UE shall conclude that the S-CSCF does not support the registration procedure as described in RFC 5626, and the S-CSCF has followed the registration procedure as described in RFC 5627 or RFC 3261, i.e., if there is a previously registered contact address, the S-CSCF replaced the old contact address and associated information with the new contact address and associated information (see bullet e) above). Upon detecting that the S-CSCF does not support the registration procedure as defined in RFC 5626, the UE shall refrain from registering any additional IMS flows for the same private identity as described in RFC 5626; or
3984: NOTE 9:	Upon replaces the old contact address with the new contact address, the S-CSCF performs the network initiated deregistration procedure for the previously registered public user identities and the associated old contact address as described in subclause 5.4.1.5. Hence, the UE will receive a NOTIFY request informing the UE about the deregistration of the old contact address. 
3985: -	if an option-tag "outbound" is present, the UE may establish additional IMS flows for the same private identity, as defined in RFC 5626;
3986: g)	store the announcement of media plane security mechanisms the P-CSCF (IMS-ALG) supports labelled with the "mediasec" header field parameter specified in subclause 7.2A.7 and received in the Security-Server header field, if any. Once the UE chooses a media security mechanism from the list received in the Security-Server header field from the server, it may initiate that mechanism on a media level when it initiates new media in an existing session; and
3987: NOTE 10:	The "mediasec" header field parameter indicates that security mechanisms are specific to the media plane.
3988: h)	if the Via header field contains a "keep" header field parameter with a value, unless the UE detects that it is not behind a NAT, start to send keep-alives associated with the registration towards the P-CSCF, as described in RFC 6223.
3989: [TS 24.229, clause 5.1.1.2.2]:
3990: On sending a REGISTER request, as defined in subclause 5.1.1.2.1, the UE shall additionally populate the header fields as follows:
3991: a)	an Authorization header field, with:
3992: -	the "username" header field parameter, set to the value of the private user identity;
3993: -	the "realm" header field parameter, set to the domain name of the home network;
3994: -	the "uri" header field parameter, set to the SIP URI of the domain name of the home network;
3995: -	the "nonce" header field parameter, set to an empty value; and
3996: -	the "response" header field parameter, set to an empty value;
3997: NOTE 1:	If the UE specifies its FQDN in the hostport parameter in the Contact header field and in the sent-by field in the Via header field, then it has to ensure that the given FQDN will resolve (e.g., by reverse DNS lookup) to the IP address that is bound to the security association.
3998: NOTE 2:	The UE associates two ports, a protected client port and a protected server port, with each pair of security association. For details on the selection of the port values see 3GPP TS 33.203.
3999: b)	additionally for the Contact header field, if the REGISTER request is protected by a security association, include the protected server port value in the hostport parameter;
4000: c)	additionally for the Via header field, for UDP, if the REGISTER request is protected by a security association, include the protected server port value in the sent-by field; and
4001: d)	a Security-Client header field set to specify the signalling plane security mechanism the UE supports, the IPsec layer algorithms the UE supports and the parameters needed for the security association setup. The UE shall support the setup of two pairs of security associations as defined in 3GPP TS 33.203. The syntax of the parameters needed for the security association setup is specified in annex H of 3GPP TS 33.203. The UE shall support the "ipsec-3gpp" security mechanism, as specified in RFC 3329. The UE shall support the IPsec layer algorithms for integrity and confidentiality protection as defined in 3GPP TS 33.203, and shall announce support for them according to the procedures defined in RFC 3329.
4002: On receiving the 200 (OK) response to the REGISTER request defined in subclause 5.1.1.2.1, the UE shall additionally:
4003: 1)	If the UE supports multiple registrations and the REGISTER request contained the "+sip.instance" header field parameter and the "reg-id" header field parameter in the Contact header field, and the "outbound" option-tag in the Supported header field, the UE shall check whether the option-tag "outbound" is present in the Require header field. If the option-tag "outbound" is present, then the UE shall use the bidirectional flow as defined in RFC 5626 as follows:
4004: a)	for UDP, the bidirectional flow consists of two unidirectional flows, i.e. the first unidirectional flow is identified with the UE's protected client port, the P-CSCF's protected server port, and the respective IP addresses. The UE uses this flow to send the requests and responses to the P-CSCF. The second unidirectional flow is identified with the P-CSCF's protected client port, the UE's protected server port and the IP addresses. The second unidirectional flow is used by the UE to receive the requests and responses from the P-CSCF; or
4005: b)	for TCP, the bidirectional flow is the TCP connection between the UE and the P-CSCF. This TCP connection was established by the UE, i.e. from the UE's protected client port and the UE's IP address to the P-CSCF's protected server port and the P-CSCF's IP address. This TCP connection is used to exchange SIP messages between the UE and the P-CSCF; and
4006: 2)	set the security association lifetime to the longest of either the previously existing security association lifetime (if available), or the lifetime of the just completed registration plus 30 seconds.
4007: NOTE 3:	If the UE receives Authentication-Info, it will proceed as described in RFC 3310.
4008: When a 401 (Unauthorized) response to a REGISTER is received the UE shall behave as described in subclause 5.1.1.5.1.
4009: [TS 24.229, clause 5.1.1.5.1]:
4010: Authentication is performed during initial registration. A UE can be re-authenticated during subsequent reregistrations, deregistrations or registrations of additional public user identities. When the network requires authentication or re-authentication of the UE, the UE will receive a 401 (Unauthorized) response to the REGISTER request.
4011: On receiving a 401 (Unauthorized) response to the REGISTER request, the UE shall:
4012: 1)	extract the RAND and AUTN parameters;
4013: 2)	check the validity of a received authentication challenge, as described in 3GPP TS 33.203 i.e. the locally calculated XMAC must match the MAC parameter derived from the AUTN part of the challenge; and the SQN parameter derived from the AUTN part of the challenge must be within the correct range; and
4014: 3)	check the existence of the Security-Server header field as described in RFC 3329. If the Security-Server header field is not present or it does not contain the parameters required for the setup of the set of security associations (see annex H of 3GPP TS 33.203), the UE shall abandon the authentication procedure and send a new REGISTER request with a new Call-ID.
4015: [TS 24.229 Rel-8, clause 5.1.1.5.1]:
4016: In the case that the 401 (Unauthorized) response to the REGISTER request is deemed to be valid the UE shall:
4017: 1)	calculate the RES parameter and derive the keys CK and IK from RAND as described in 3GPP TS 33.203;
4018: 2)	set up a temporary set of security associations for this registration based on the static list and parameters the UE received in the 401 (Unauthorized) response and its capabilities sent in the Security-Client header field in the REGISTER request. The UE sets up the temporary set of security associations using the most preferred mechanism and algorithm returned by the P-CSCF and supported by the UE and using IK and CK (only if encryption enabled) as the shared key. The UE shall use the parameters received in the Security-Server header field to setup the temporary set of security associations. The UE shall set a temporary SIP level lifetime for the temporary set of security associations to the value of reg-await-auth timer; and
4019: 3)	send another REGISTER request towards the protected server port indicated in the response using the temporary set of security associations to protect the message. The header fields are populated as defined for the initial REGISTER request that was challenged with the received 401 (Unauthorized) response, with the addition that the UE shall include an Authorization header field containing:
4020: -	the "realm" header field parameter set to the value as received in the "realm" WWW-Authenticate header field parameter;
4021: -	the "username" header field parameter, set to the value of the private user identity;
4022: -	the "response" header field parameter that contains the RES parameter, as described in RFC 3310;
4023: -	the "uri" header field parameter, set to the SIP URI of the domain name of the home network;
4024: -	the "algorithm" header field parameter, set to the value received in the 401 (Unauthorized) response; and
4025: -	the "nonce" header field parameter, set to the value received in the 401 (Unauthorized) response. 
4026: 	The UE shall also insert the Security-Client header field that is identical to the Security-Client header field that was included in the previous REGISTER request (i.e. the REGISTER request that was challenged with the received 401 (Unauthorized) response). The UE shall also insert the Security-Verify header field into the request, by mirroring in it the content of the Security-Server header field received in the 401 (Unauthorized) response. The UE shall set the Call-ID of the security association protected REGISTER request which carries the authentication challenge response to the same value as the Call-ID of the 401 (Unauthorized) response which carried the challenge.
4027: [TS 24.229 Rel-9, clause 5.1.1.5.1]:
4028: In the case that the 401 (Unauthorized) response to the REGISTER request is deemed to be valid the UE shall:
4029: 1)	calculate the RES parameter and derive the keys CK and IK from RAND as described in 3GPP TS 33.203 [19];
4030: 2)	set up a temporary set of security associations for this registration based on the static list and parameters the UE received in the 401 (Unauthorized) response and its capabilities sent in the Security-Client header field in the REGISTER request. The UE sets up the temporary set of security associations using the most preferred mechanism and algorithm returned by the P-CSCF and supported by the UE and using IK and CK (only if encryption enabled) as the shared key. The UE shall use the parameters received in the Security-Server header field to setup the temporary set of security associations. The UE shall set a temporary SIP level lifetime for the temporary set of security associations to the value of reg-await-auth timer;
4031: 3)	store the announcement of the media plane security mechanisms the P-CSCF (IMS-ALG) supports received in the Security-Server header field and labelled with the "mediasec" header field parameter specified in subclause 7.2A.7, if any; and
4032: NOTE 1:	The "mediasec" header field parameter indicates that security mechanisms are specific to the media plane.
4033: 4)	send another REGISTER request towards the protected server port indicated in the response using the temporary set of security associations to protect the message. The header fields are populated as defined for the initial REGISTER request that was challenged with the received 401 (Unauthorized) response, with the addition that the UE shall include an Authorization header field containing:
4034: -	the "realm" header field parameter set to the value as received in the "realm" WWW-Authenticate header field parameter;
4035: -	the "username" header field parameter, set to the value of the private user identity;
4036: -	the "response" header field parameter that contains the RES parameter, as described in RFC 3310 [49];
4037: -	the "uri" header field parameter, set to the SIP URI of the domain name of the home network;
4038: -	the "algorithm" header field parameter, set to the value received in the 401 (Unauthorized) response; and
4039: -	the "nonce" header field parameter, set to the value received in the 401 (Unauthorized) response. 
4040: 	The UE shall also insert the Security-Client header field that is identical to the Security-Client header field that was included in the previous REGISTER request (i.e. the REGISTER request that was challenged with the received 401 (Unauthorized) response). The UE shall also insert the Security-Verify header field into the request, by mirroring in it the content of the Security-Server header field received in the 401 (Unauthorized) response. The UE shall set the Call-ID of the security association protected REGISTER request which carries the authentication challenge response to the same value as the Call-ID of the 401 (Unauthorized) response which carried the challenge.
4041: [TS 24.229, clause 5.1.1.5.1]:
4042: On receiving the 200 (OK) response for the security association protected REGISTER request registering a public user identity with the associated contact address, the UE shall:
4043: -	change the temporary set of security associations to a newly established set of security associations, i.e. set its SIP level lifetime to the longest of either the previously existing set of security associations SIP level lifetime, or the lifetime of the just completed registration plus 30 seconds; and
4044: -	if this is the only set of security associations available toward the P-CSCF, use the newly established set of security associations for further messages sent towards the P-CSCF. If there are additional sets of security associations (e.g. due to registration of multiple contact addresses), the UE can either use them or use the newly established set of security associations for further messages sent towards the P-CSCF as appropriate.
4045: NOTE 2:	If the UE has registered multiple contact addresses, the UE can either send requests towards the P-CSCF over the newly established set of security associations, or use different UE's contact address and associated set of security associations when sending the requests towards the P-CSCF. Responses towards the P-CSCF that are sent via UDP will be sent over the same set of security associations that the related request was received on. Responses towards the P-CSCF that are sent via TCP will be sent over the same set of security associations that the related request was received on.
4046: When the first request or response protected with the newly established set of security associations is received from the P-CSCF or when the lifetime of the old set of security associations expires, the UE shall delete the old set of security associations and related keys it may have with the P-CSCF after all SIP transactions that use the old set of security associations are completed.
4047: [TS 24.229, clause 5.1.1.3]:
4048: Upon receipt of a 2xx response to the initial registration, the UE shall subscribe to the reg event package for the public user identity registered at the user's registrar (S-CSCF) as described in RFC 3680.
4049: The UE shall subscribe to the reg event package upon registering a new contact address via an initial registration procedure. If the UE receives a NOTIFY request via the newly established subscription dialog and via the previously established subscription dialogs (there will be at least one), the UE may terminate the previously established subscription dialogs and keep only the newly established subscription dialog.
4050: The UE shall use the default public user identity for subscription to the registration-state event package, if the public user identity that was used for initial registration is a barred public user identity. The UE may use either the default public user identity or the public user identity used for initial registration for the subscription to the registration-state event package, if the initial public user identity that was used for initial registration is not barred.
4051: [TS 24.229 Rel-8, clause 5.1.1.3]:
4052: On sending a SUBSCRIBE request, the UE shall populate the header fields as follows:
4053: a)	a Request-URI set to the resource to which the UE wants to be subscribed to, i.e. to a SIP URI that contains the public user identity used for subscription;
4054: b)	a From header field set to a SIP URI that contains the public user identity used for subscription;
4055: c)	a To header field set to a SIP URI that contains the public user identity used for subscription;
4056: d)	an Event header field set to the "reg" event package;
4057: e)	an Expires header field set to 600 000 seconds as the value desired for the duration of the subscription;
4058: f)	if available to the UE (as defined in the access technology specific annexes for each access technology), a P-Access-Network-Info header field set as specified for the access network technology (see subclause 7.2A.4); and
4059: g)	a Contact header field set to contain:.
4060: the same IP address or FQDN, and if multiple registrations is supported, its instance ID ("+sip.instance" header field parameter) and an "ob" SIP URI parameter as described in RFC 5626;
4061: -	if IMS AKA or SIP digest with TLS is being used as a security mechanism, the protected server port value as in the initial registration; and
4062: -	if SIP digest without TLS, NASS-IMS bundled authentication or GPRS-IMS-Bundled authentication is being used as a security mechanism, the port value of an unprotected port where the UE expects to receive subsequent mid-dialog requests. The UE shall set the unprotected port value to the port value used in the initial REGISTER request.
4063: Upon receipt of a 2xx response to the SUBSCRIBE request, the UE shall store the information for the established dialog and the expiration time as indicated in the Expires header field of the received response.
4064: [TS 24.229 Rel-9, clause 5.1.1.3]:
4065: On sending a SUBSCRIBE request, the UE shall populate the header fields as follows:
4066: a)	a Request-URI set to the resource to which the UE wants to be subscribed to, i.e. to a SIP URI that contains the public user identity used for subscription;
4067: b)	a From header field set to a SIP URI that contains the public user identity used for subscription;
4068: c)	a To header field set to a SIP URI that contains the public user identity used for subscription;
4069: d)	an Event header field set to the "reg" event package;
4070: e)	an Expires header field set to 600 000 seconds as the value desired for the duration of the subscription;
4071: f)	void; and
4072: g)	void.
4073: Upon receipt of a 2xx response to the SUBSCRIBE request, the UE shall store the information for the established dialog and the expiration time as indicated in the Expires header field of the received response.
4074: [TS 24.229, clause 5.1.2.1]:
4075: Upon receipt of a 2xx response to the SUBSCRIBE request the UE shall maintain the generated dialog (identified by the values of the Call-ID header field, and the values of tags in To and From header fields).
4076: Upon receipt of a NOTIFY request on the dialog which was generated during subscription to the reg event package the UE shall perform the following actions:
4077: -	if a state attribute "active", i.e. registered is received for one or more public user identities, the UE shall store the indicated public user identities as registered;
4078: -	if a state attribute "active" is received, and the UE supports GRUU (see table A.4, item A.4/53), then for each public user identity indicated in the notification that contains a <pub-gruu> element or a <temp-gruu> element or both (as defined in RFC 5628) then the UE shall store the value of those elements in association with the public user identity;
4079: -	if a state attribute "terminated", i.e. deregistered is received for one or more public user identities, the UE shall store the indicated public user identities as deregistered and shall remove any associated GRUUs.
4080: NOTE 1:	There may be public user identities which are automatically registered within the registrar (S-CSCF) of the user upon registration of one public user identity or when S-CSCF receives a Push-Profile-Request (PPR) from the HSS (as described in 3GPP TS 29.228) changing the status of a public user identity associated with a registered implicit set from barred to non-barred. Usually these automatically or implicitly registered public user identities belong to the same service profile of the user and they might not be available within the UE. The implicitly registered public user identities may also belong to different service profiles. The here-described procedures provide a different mechanism (to the 200 (OK) response to the REGISTER request) to inform the UE about these automatically registered public user identities.
4081: NOTE 2:	RFC 5628 provides guidance on the management of temporary GRUUs, utilizing information provided in the reg event notification.
4082: [TS 24.229, clause 5.1.2A.1.1]:
4083: The procedures of this subclause are general to all requests and responses, except those for the REGISTER method.
4084: When the UE sends any request using either a given contact address, or to the registration flow and the associated contact address the UE shall:
4085: -	if IMS AKA is in use as a security mechanism:
4086: a)	if the UE has not obtained a GRUU, populate the Contact header field of the request with the protected server port and the respective contact address; and
4087: b)	include the protected server port and the respective contact address in the Via header field entry relating to the UE;
4088: -	if SIP digest without TLS is in use as a security mechanism:
4089: a)	if the UE has not obtained a GRUU, populate the Contact header field of the request with the port value of an unprotected port and the contact address where the UE expects to receive subsequent mid-dialog requests; and
4090: b)	populate the Via header field of the request with the port value of an unprotected port and the respective contact address where the UE expects to receive responses to the request; 
4091: ...
4092: If available to the UE (as defined in the access technology specific annexes for each access technology), the UE shall insert a P-Access-Network-Info header field into any request for a dialog, any subsequent request (except ACK requests and CANCEL requests) or response (except CANCEL responses) within a dialog or any request for a standalone method (see subclause 7.2A.4).
4093: NOTE 13:	During the dialog, the points of attachment to the IP-CAN of the UE may change (e.g. UE connects to different cells). The UE will populate the P-Access-Network-Info header field in any request or response within a dialog with the current point of attachment to the IP-CAN (e.g. the current cell information).
4094: The UE shall build a proper preloaded Route header field value for all new dialogs and standalone transactions. The UE shall build a list of Route header field values made out of the following, in this order:
4095: a)	the P-CSCF URI containing the IP address or the FQDN learnt through the P-CSCF discovery procedures; and
4096: b)	the P-CSCF port based on the security mechanism in use:
4097: -	if IMS AKA or SIP digest with TLS is in use as a security mechanism, the protected server port learnt during the registration procedure;
4098: -	if SIP digest without TLS, NASS-IMS bundled authentication or GPRS-IMS-Bundled authentication is in use as a security mechanism, the unprotected server port used during the registration procedure;
4099: c)	and the values received in the Service-Route header field saved from the 200 (OK) response to the last registration or re-registration of the public user identity with associated contact address. 
4100: [TS 24.341, clause 5.3.2.2]
4101: On sending a REGISTER request, the SM-over-IP receiver shall indicate its capability to receive traditional short messages over IMS network by including a "+g.3gpp.smsip" parameter into the Contact header according to RFC 3840.
4102: Reference(s)
4103: 3GPP TS 24.229 [10], clauses 5.1.1.1A, 5.1.1.2.1 5.1.1.2, 5.1.1.35.1.1.5.1, 5.1.2.1, 5.1.2A.1, C.2 and TS 24.341, clause 5.3.2.2.
4104: 8.1.3	Test purpose
4105: 1)	To verify that UE correctly derives a private user identity, a temporary public user identity and a home network domain name from the IMSI parameter in the USIM if no ISIM is available on the UICC, according to the procedures described in 3GPP TS 23.003 [32] clause 13 or alternatively uses the values retrieved from ISIM, if ISIM is present; and
4106: 2)	To verify that the UE sends a correctly composed initial REGISTER request to S-CSCF via the discovered P-CSCF, according to 3GPP TS 24.229 [10] clause 5.1.1.2; and TS 24.341 [90] clause 5.3.2.2 (if UE supports SM-over-IP receiver marked as yes)
4107: 3)	To verify that after receiving a valid 401 (Unauthorized) response from S-CSCF for the initial REGISTER sent, the UE correctly authenticates itself by sending another REGISTER request with correctly composed Authorization header using AKAv1-MD5 algorithm (as described in RFC 3310 [17]); and
4108: 4)	To verify that the UE announces to support the "ipsec-3gpp" security mechanism together the IPsec layer algorithms for integrity (Rel-5 onwards) and confidentiality (Rel-6 onwards) protection (as defined in 3GPP TS 33.203)according to the procedures defined in RFC 3329 [21]; and
4109: 5)	To verify that the UE supports the IPsec layer algorithms for integrity (Rel-5 onwards) and confidentiality (Rel-6 onwards) protection as defined in 3GPP TS 33.203and uses the one that is preferred by the P-CSCF according to the procedures defined in RFC 3329 [21]; and
4110: 6)	To verify that the UE sets up two pairs of security associations as defined in 3GPP TS 33.203 [14] clause 7 and uses those for sending the REGISTER request to authenticate itself and for sending any other subsequent request; and
4111: 7)	To verify that after receiving a valid 200 OK response from S-CSCF for the REGISTER sent for authentication, the UE stores the default public user identity and information about barred user identities; and
4112: 8)	To verify that after receiving a valid 200 OK response from S-CSCF for the REGISTER sent for authentication, the UE subscribes to the reg event package for the public user identity registered at the users registrar (S-CSCF) as described in RFC 3680 [22]; and
4113: 9)	To verify that the UE uses the default public user identity for subscription to the registration-state event package, when the public user identity that was used for initial registration is a barred public user identity; and
4114: 10)	To verify that the UE uses the stored service route for routing the SUBSCRIBE sent; and
4115: 11)	To verify that after receiving a valid 200 OK response from S-CSCF to the SUBSCRIBE sent for registration event package, the UE maintains the generated dialog; and
4116: 12)	To verify that after receiving a valid NOTIFY for the registration event package, the UE will update and store the registration state of the indicated public user identities accordingly (as specified in RFC 3680 [22] clause 5); and
4117: 13)	To verify that the UE responds the received valid NOTIFY with 200 OK.
4118: 8.1.4	Method of test
4119: Initial conditions
4120: UE contains either ISIM and USIM applications or only USIM application on UICC. UE is not registered to IMS services.
4121: SS is configured with the IMSI within the USIM application, the home domain name, public and private user identities together with the shared secret key of IMS AKA algorithm, related to the IMS private user identity (IMPI) that is configured on the UICC card equipped into the UE. SS is listening to SIP default port 5060 for both UDP and TCP protocols. SS is able to perform AKAv1-MD5 authentication algorithm for that IMPI, according to 3GPP TS 33.203 [14] clause 6.1 and RFC 3310 [17].
4122: Test procedure
4123: 1-11)	Execute the generic test procedure in Annex C.2 up to the last step.
4124: NOTE:	This test case shall be run twice in order to test that the UE correctly supports both HMAC-MD5-96 and HMAC-SHA-1-96 algorithms. For each test round the name of the corresponding algorithm shall be configured into px_IMS_IpSecAlgorithm PIXIT.
4125: Expected sequence
4126: Step
4127: Direction
4128: Message
4129: Comment
4131: UE
4132: SS
4135: 1-11
4137:  Steps defined in C.2
4138:  IMS Registration
4140: 8.1.5	Test requirements
4141: If the UICC card equipped to the UE contains ISIM, the UE must read the following parameters from ISIM (instead of deriving them from USIM) and use they for the REGISTER requests:
4142: -	the private user identity; and
4143: -	the temporary public user identity; and
4144: -	the home network domain name.
4145: Step 3: SS shall check that in accordance to the 3GPP TS 24.229 [10] clause 5.1.1.5 the UE sends another REGISTER request as follows:
4146: a)	the UE sets up the temporary set of security associations between the ports announced in Security-Client header (UE) in the REGISTER request and Security-Server header (SS) in the 401 Unauthorized response; and
4147: b)	the UE uses the most preferred mechanism and algorithm returned by the SS and supported by the UE for the temporary set of security associations; and
4148: c)	the UE uses IK derived from RAND as the shared key for integrity and confidentiality protection (if the UE supports IPSec ESP confidentiality protection) for the temporary set of security associations; and
4149: d)	the UE sends the second REGISTER over the temporary set of security associations; and
4150: Step 5: SS shall check that, in accordance to the 3GPP TS 24.229 [10] clause 5.1.1.3, the UE sends a SUBSCRIBE request for registration event package over the newly established set of security associations. 
4151: NOTE:	If the UE specifies its FQDN in the host parameter in the Contact header and in the sent-by field in the Via header (within any of the request sent by the UE), then SS has to ensure that the given FQDN will resolve (e.g., by reverse DNS lookup) to the IP address that is bound to the security association (or to the unprotected port in the initial REGISTER).
```

## 8.2 User Initiated Re-Registration（行 4152-4344；used_by: TC-014）

关键官方标记：`8.2.1	Definition`、`8.2.2	Conformance requirement`、`8.2.3	Test purpose`、`8.2.4	Method of test`、`8.2.5	Test requirements`、`60 seconds`、`600 seconds`、`1200 seconds`、`Security-Client`、`P-Associated-URI`

```text
4152: 8.2	User Initiated Re-Registration
4153: 8.2.1	Definition 
4154: Test to verify that the UE can re-register a previously registered public user identity at any time. This process is described in 3GPP TS 24.229 [10], clause 5.1.1.4. 
4155: 8.2.2	Conformance requirement
4156: [TS 24.229, clause 5.1.1.4.1]:
4157: The UE can perform the reregistration of a previously registered public user identity bound to any one of its contact addresses and the associated set of security associations or TLS sessions at any time after the initial registration has been completed.
4158: The UE can perform the reregistration of a previously registered public user identity over any existing set of security associations or TLS session that is associated with the related contact address.
4159: The UE can perform the reregistration of a previously registered public user identity via an initial registration as specified in subclause 5.1.1.2, when binding the previously registered public user identity to new contact address.
4160: The UE can perform registration of additional public user identities at any time after the initial registration has been completed. The UE shall perform the registration of additional public user identities either:
4161: -	over the existing set of security associations or TLS sessions, if appropriate to the security mechanism in use, that is associated with the related contact address; or
4162: -	via an initial registration as specified in subclause 5.1.1.2.
4163: The UE can fetch bindings as defined in RFC 3261 at any time after the initial registration has been completed. The procedure for fetching bindings is the same as for a reregistration except that the REGISTER request does not contain a Contact header field.
4164: Unless either the user or the application within the UE has determined that a continued registration is not required the UE shall reregister an already registered public user identity either 600 seconds before the expiration time if the previous registration was for greater than 1200 seconds, or when half of the time has expired if the previous registration was for 1200 seconds or less, or when the UE intends to update its capabilities according to RFC 3840 or when the UE needs to modify the ICSI values that the UE intends to use in a g.3gpp.icsi-ref media feature tag or IARI values that the UE intends to use in the g.3gpp.iari-ref media feature tag.
4165: When sending a protected REGISTER request, the UE shall use a security association or TLS session associated with the contact address used to send the request, see 3GPP TS 33.203, established as a result of an earlier initial registration.
4166: The UE shall extract or derive a public user identity, the private user identity, and the domain name to be used in the Request-URI in the registration, according to the procedures described in subclause 5.1.1.1A or subclause 5.1.1.1B.
4167: On sending a REGISTER request that does not contain a challenge response, the UE shall populate the header fields as follows:
4168: a)	a From header field set to the SIP URI that contains the public user identity to be registered;
4169: b)	a To header field set to the SIP URI that contains the public user identity to be registered;
4170: c)	a Contact header field set to include SIP URI(s) that contain(s) in the hostport parameter the IP address or FQDN of the UE, and containing the instance ID of the UE in the "+sip.instance" header field parameter, if the UE supports GRUU (see table A.4, item A.4/53) or multiple registrations. If the UE support multiple registrations, it shall include "reg-id" header field as described in RFC 5626. The UE shall include all supported ICSI values (coded as specified in subclause 7.2A.8.2) in a g.3gpp.icsi-ref media feature tag as defined in subclause 7.9.2 and RFC 3840 for the IMS communication it intends to use, and IARI values (coded as specified in subclause 7.2A.9.2), for the IMS applications it intends to use in a g.3gpp.iari-ref media feature tag as defined in subclause 7.9.3 and RFC 3840;
4171: d)	a Via header field set to include the IP address or FQDN of the UE in the sent-by field. For the TCP, the response is received on the TCP connection on which the request was sent. If the UE previously has previously negotiated sending of keep-alives associated with the registration, it shall include a "keep" header field parameter with no value in the Via header field, in order to indicate continuous support to send keep-alives, as described in draft-ietf-sipcore-keep;
4172: e)	a registration expiration interval value, set to 600 000 seconds as the value desired for the duration of the registration;
4173: NOTE 1:	The registrar (S-CSCF) might decrease the duration of the registration in accordance with network policy. Registration attempts with a registration period of less than a predefined minimum value defined in the registrar will be rejected with a 423 (Interval Too Brief) response.
4174: f)	a Request-URI set to the SIP URI of the domain name of the home network used to address the REGISTER request;
4175: g)	the Supported header field containing the option-tag "path", and if GRUU is supported, the option-tag "gruu";
4176: h)	if available to the UE (as defined in the access technology specific annexes for each access technology), a P-Access-Network-Info header field set as specified for the access network technology (see subclause 7.2A.4); and
4177: i)	a Security-Client header field to announce the media plane security mechanisms the UE supports, if any, according to the procedures described in draft-dawes-dispatch-mediasec-parameter.
4178: NOTE 2:	Security mechanisms that apply to the media plane are distinguished by the "mediasec" header field parameter.
4179: On receiving the 200 (OK) response to the REGISTER request, the UE shall:
4180: a)	bind the new expiration time of the registration for this public user identity found in the To header field value to the contact address used in this registration;
4181: b)	store the list of service route values contained in the Service-Route header field and bind the list to the contact address used in registration, in order to build a proper preloaded Route header field value for new dialogs and standalone transactions when using the respective contact address;
4182: NOTE 3:	If the list of Service-Route headers saved from a previous registration and bound to this contact address and the associated set of security associations or TLS session already exist, then the received list of Service-Route headers replaces the old list.
4183: NOTE 4:	The UE can utilize additional URIs contained in the P-Associated-URI header field, e.g. for application purposes.
4184: c)	find the Contact header field within the response that matches the one included in the REGISTER request. If this contains a "pub-gruu" header field parameter or a "temp-gruu" header field parameter or both, and the UE supports GRUU (see table A.4, item A.4/53), then store the value of those parameters as the GRUUs for the UE in association with the public user identity and the contact address that was registered;
4185: d)	store the announcement of the media plane security mechanisms the P-CSCF (IMS-ALG) supports received in the Security-Server header field, if any, according to the procedures described in draft-dawes-dispatch-mediasec-parameter; and
4186: NOTE 5:	Security mechanisms that apply to the media plane are distinguished by the "mediasec" header field parameter.
4187: e)	if the Via header field contains a "keep" header field parameter with a value, continue to send keep-alives as described in draft-ietf-sipcore-keep, towards the P-CSCF.
4188: When a 401 (Unauthorized) response to a REGISTER is received the UE shall behave as described in subclause 5.1.1.5.1.
4189: [TS 24.229, clause 5.1.1.4.2]:
4190: On sending a REGISTER request, as defined in subclause 5.1.1.4.1, the UE shall additionally populate the header fields as follows:
4191: a)	an Authorization header field, with:
4192: -	the "username" header field parameter set to the value of the private user identity;
4193: -	the "realm" header field parameter directive, set to the value as received in the "realm" WWW-Authenticate header field parameter;
4194: -	the "uri" header field parameter, set to the SIP URI of the domain name of the home network;
4195: -	the "nonce" header field parameter, set to last received nonce value; and
4196: -	the "response" header field parameter, set to the last calculated response value;
4197: NOTE 1:	If the UE specifies its FQDN in the hostport parameter in the Contact header field and in the sent-by field in the Via header field, then it has to ensure that the given FQDN will resolve (e.g., by reverse DNS lookup) to the IP address that is bound to the security association.
4198: NOTE 2:	The UE associates two ports, a protected client port and a protected server port, with each pair of security associations. For details on the selection of the protected port value see 3GPP TS 33.203.
4199: NOTE 3:	If the UE is setting up an additional registration using procedures specified in RFC 5626 and the UE accesses the network through 3GPP or 3GPP2 systems without any NAT, the flow is considered to be "logical flow".
4200: b)	additionally for the Contact header field, include the protected server port value in the hostport parameter;
4201: c)	additionally for the Via header field, for UDP, if the REGISTER request is protected by a security association, include the protected server port value in the sent-by field;
4202: d)	a Security-Client header field, set to specify the signalling plane security mechanism it supports, the IPsec layer algorithms for security and confidentiality protection it supports and the new parameter values needed for the setup of two new pairs of security associations. For further details see 3GPP TS 33.203 and RFC 3329; and
4203: e)	a Security-Verify header field that contains the content of the Security-Server header field received in the 401 (Unauthorized) response of the last successful authentication.
4204: On receiving the 200 (OK) response to the REGISTER request, the UE shall additionally:
4205: a)	set the security association lifetime associated with this contact address and the associated set of security associations to the longest of either the previously existing security association lifetime, or the lifetime of the just completed registration plus 30 seconds.
4206: NOTE 4:	If the UE receives Authentication-Info, it will proceed as described in RFC 3310.
4207: Reference(s)
4208: 3GPP TS 24.229 [10], clauses 5.1.1.4.1 and 5.1.1.4.2. 
4209: 8.2.3	Test purpose
4210: 1)	To verify that the UE can re-register a previously registered public user identity at either 600 seconds before the expiration time if the initial registration was for greater than 1200 seconds, or when half of the time has expired if the initial registration was for 1200 seconds or less; and 
4211: 2)	Extract or derive a public user identity, the private user identity, and the domain name to be used in the Request-URI in the registration; and
4212: 3)	To verify that the UE populates the header field in the REGISTER request with From, To, Via, Contact, Authorization, Expires, Security-Client, Security-verify, Supported, and P-Access-Network-Info headers; and
4213: 4)	Upon receiving 200 OK for REGISTER, the UE shall store the new expiration time of the registration for this public user identity, the list of URIs contained in the P-Associated-URI header value and use these values in the next re-register request.
4214: 8.2.4	Method of test
4215: Initial conditions
4216: UE contains either ISIM and USIM applications or only USIM application on UICC. UE is not registered to IMS services, but has an active PDP context and has discovered the SS as P-CSCF by executing the generic test procedure in Annex C.2 up to step 3.
4217: SS is configured with the shared secret key of IMS AKA algorithm, related to the IMS private user identity (IMPI) configured on the UICC card equipped into the UE. SS is able to perform AKAv1-MD5 authentication algorithm for that IMPI, according to 3GPP TS 33.203 [14] clause 6.1 and RFC 3310 [17].
4218: Test procedure
4219: 1-8C) The same procedure as in Annex C.2 is used with the exception that the SS sets the expiration time to 120 seconds in Step 4.
4220: 9)	Before half of the time has expired from the initial registration SS receives re-register message request with the From, To, Via, Contact, Authorization, Expires, Security-Client, Security-verify, Supported, and P-Access-Network-Info header fields.
4221: 10)	SS responds to the REGISTER request with valid 200 OK response with the list of URIs contained in the P-Associated-URI header value, the new expiration time (1200 seconds) of the registration for this public user identity.
4222: 11)	SS waits for the REGISTER request and verifies it is received at least 600 seconds before the expected expiration time.
4223: 12)	SS responds to the REGISTER request with valid 200 OK response with the list of URIs contained in the P-Associated-URI header value, the new expiration time (1800 seconds) of the registration for this public user identity.
4224: 13)	SS waits for the REGISTER request and verifies it is received at least 600 seconds before the expected expiration time.
4225: 14)	SS responds to the REGISTER request with valid 200 OK response. SS shall populate the headers of the 200 OK response according to the 200 response for REGISTER common message definition.
4226: Expected sequence
4227: Step
4228: Direction
4229: Message
4230: Comment
4232: UE
4233: SS
4236: 1-8C
4238: Messages 1-11 of Annex C.2
4239: The same messages as in Annex C.2 are used with the exception that in Step 7 of C.2, the SS responds with 200 OK indicating 120 seconds expiration time.
4240: 9
4241: -->
4242: REGISTER
4243: The SS receives REGISTER from the UE 60 seconds before the expiration time set in the initial registration request.
4244: 10
4245: <--
4246: 200 OK
4247: The SS responds with 200 OK indicating 1200 seconds expiration time.
4248: 11
4249: -->
4250: REGISTER
4251: The SS receives REGISTER from the UE 600 seconds before the expiration time set in step 10.
4252: 12
4253: <--
4254: 200 OK
4255: The SS responds with 200 OK indicating 1800 seconds expiration time.
4256: 13
4257: -->
4258: REGISTER
4259: The SS receives REGISTER from the UE 600 seconds before the expiration time set in step 12
4260: 14
4261: <--
4262: 200 OK
4263: The SS responds with 200 OK indicating the default expiration time.
4265: Specific Message Contents
4266: Messages in Step 1-8C
4267: Messages in Step 1-8C are the same as those specified in Annex C.2 with the following exception for the 200 OK for REGISTER in Step 7 of C.2:
4268: Use the default message "200 OK for REGISTER" in annex A.1.3 with the following exceptions:
4269: Header/param
4270: Value/remark
4271: Contact
4273: 	expires
4274: 120
4276: REGISTER (Step 9)
4277: Use the default message "REGISTER" in annex A.1.1 with conditions A2 "Subsequent REGISTER sent over security associations" and A17 "UE initiated IMS re-registration or de-registration" and with the following exceptions:
4278: Header/param
4279: Value/remark
4280: Security-Client
4282: 	spi-c
4283: new SPI number of the inbound SA at the protected client port, shall be different than in step 3
4284: 	spi-s
4285: new SPI number of the inbound SA at the protected server port, shall be different than in step 3
4286: 	port-c
4287: new protected client port, shall be different than in step 3
4288: 	port-s
4289: Same value as in the previous REGISTER
4291: 200 OK for REGISTER (Step 10)
4292: Use the default message "200 OK for REGISTER" in annex A.1.3 with the following exceptions:
4293: Header/param
4294: Value/remark
4295: Contact
4297: 	expires
4298: 1200
4300: REGISTER (Step 11)
4301: Use the default message "REGISTER" in annex A.1.1 with conditions A2 "Subsequent REGISTER sent over security associations" and A17 "UE initiated IMS re-registration or de-registration" and with the following exceptions:
4302: Header/param
4303: Value/remark
4304: Security-Client
4306: 	spi-c
4307: new SPI number of the inbound SA at the protected client port, shall be different than in step 3 but may or may not be the same as in step 9
4308: 	spi-s
4309: new SPI number of the inbound SA at the protected server port, shall be different than in step 3 but may or may not be the same as in step 9
4310: 	port-c
4311: new protected client port, shall be different than in step 3 but may or may not be the same as in step 9
4312: 	port-s
4313: Same value as in the previous REGISTER
4315: 200 OK for REGISTER (Step 12)
4316: Use the default message "200 OK for REGISTER" in annex A.1.3 with the following exceptions:
4317: Header/param
4318: Value/remark
4319: Contact
4321: 	expires
4322: 1800
4324: REGISTER (Step 13)
4325: Use the default message "REGISTER" in annex A.1.1 with conditions A2 "Subsequent REGISTER sent over security associations" and A17 "UE initiated IMS re-registration or de-registration" and with the following exceptions:
4326: Header/param
4327: Value/remark
4328: Security-Client
4330: 	spi-c
4331: new SPI number of the inbound SA at the protected client port, shall be different than in step 3 but may or may not be the same as in step 9 or step 11
4332: 	spi-s
4333: new SPI number of the inbound SA at the protected server port, shall be different than in step 3 but may or may not be the same as in step 9 or step 11
4334: 	port-c
4335: new protected client, shall be different than in step 3 but may or may not be the same as in step 9 or step 11
4336: 	port-s
4337: Same value as in the previous REGISTER
4339: 200 OK for REGISTER (Step 14)
4340: Use the default message "200 OK for REGISTER" in annex A.1.3.
4341: 8.2.5	Test requirements
4342: 1.	The UE shall in step 9 send the REGISTER request within 60 seconds from the time instant that it receives 200 OK in step 4 from the SS.
4343: 2.	The UE shall in step 11 send the REGISTER request within 600 seconds from the time instant that it receives 200 OK from the SS in step 10.
4344: 3.	The UE shall in step 13 send the REGISTER request within 1200 seconds from the time instant that it receives 200 OK from the SS in step 12. 
```

## 9.1 Invalid Behaviour - MAC Parameter Invalid（行 5452-5602；used_by: TC-013）

关键官方标记：`9.1.1	Definition`、`9.1.2	Conformance requirement`、`9.1.3	Test purpose`、`9.1.4	Method of test`、`9.1.5	Test requirements`、`MAC value in AUTN should be incorrect`、`contains no AUTS directive`、`empty response directive`、`does not create a temporary set of security associations`

```text
5452: 9.1	Invalid Behaviour - MAC Parameter Invalid 
5453: 9.1.1	Definition
5454: To test that the UE when receiving a 401 (Unauthorized) response with an invalid MAC value to its initial REGISTER request behaves correctly. This procedure is described in 3GPP TS 24.229 [10] clause 5.1.1.5. 
5455: 9.1.2	Conformance requirement
5456: [TS 24.229, clause 5.1.1.5.1]
5457: Authentication is performed during initial registration. A UE can be re-authenticated during subsequent reregistrations, deregistrations or registrations of additional public user identities. When the network requires authentication or re-authentication of the UE, the UE will receive a 401 (Unauthorized) response to the REGISTER request.
5458: On receiving a 401 (Unauthorized) response to the REGISTER request, the UE shall:
5459: 1)	extract the RAND and AUTN parameters;
5460: 2)	check the validity of a received authentication challenge, as described in 3GPP TS 33.203 [19] i.e. the locally calculated XMAC must match the MAC parameter derived from the AUTN part of the challenge; and the SQN parameter derived from the AUTN part of the challenge must be within the correct range; and
5461: ...
5462: [TS 24.229 Rel-12, clause 5.1.1.5.3]
5463: If, in a 401 (Unauthorized) response, either the MAC or SQN is incorrect the UE shall respond with a further REGISTER indicating to the S-CSCF that the challenge has been deemed invalid as follows:
5464: -	in the case where the UE deems the MAC parameter to be invalid the subsequent REGISTER request shall contain no "auts" Authorization header field parameter and an empty "response" Authorization header field parameter, i.e. no authentication challenge response;
5465: -	in the case where the UE deems the SQN to be out of range, the subsequent REGISTER request shall contain the "auts" Authorization header field parameter (see 3GPP TS 33.102 [18]).
5466: NOTE:	In the case of the SQN being out of range, a "response" Authorization header field parameter can be included by the UE, based on the procedures described in RFC 3310 [49].
5467: Whenever the UE detects any of the above cases, the UE shall:
5468: -	send the REGISTER request using an existing set of security associations, if available (see 3GPP TS 33.203 [19]);
5469: -	populate a new Security-Client header field within the REGISTER request and associated contact address, set to specify the security mechanisms it supports, the IPsec layer algorithms for integrity and confidentiality protection it supports and the parameters needed for the new security association setup. These parameters shall contain new values for spi_uc, spi_us and port_uc; and 
5470: -	not create a temporary set of security associations.
5471: 9.1.3	Test purpose
5472: 1)	To verify that after receiving a 401 (Unauthorized) response for the initial REGISTER sent, the UE checks that the locally calculated XMAC matches the MAC parameter derived from the AUTN part of the challenge.
5473: 2)	If the value of MAC derived from the AUTN part of the 401 (Unauthorized) response received by the UE does not match the value of locally calculated XMAC:
5474: -	the UE responds with a further REGISTER indicating that the challenge has been deemed invalid; and
5475: -	this subsequent REGISTER request contains no "auts" Authorization header field parameter and an empty "response" Authorization header field parameter, i.e. no authentication challenge response; and
5476: -	the UE populates a new Security-Client header field within the REGISTER request and associated contact address, set to specify the security mechanism it supports, the IPsec layer algorithms it supports and the parameters needed for the new security association setup. These parameters contain new values for spi_uc, spi_us and port_uc; and
5477: -	the UE does not create a temporary set of security associations.
5478: 9.1.4	Method of test
5479: Initial conditions
5480: UE contains either ISIM and USIM applications or only USIM application on UICC. UE is not registered to IMS services, but executed the generic test procedure in Annex C.2 up to step 3.
5481: SS is configured with the shared secret key of IMS AKA algorithm, related to the IMS private user identity (IMPI) configured on the UICC card equipped into the UE. SS is able to perform AKAv1-MD5 authentication algorithm for that IMPI, according to 3GPP TS 33.203 [14] clause 6.1 and RFC 3310 [17]. SS is listening to SIP default port 5060 for both UDP and TCP protocols.
5482: Test procedure
5483: 1)	IMS registration is initiated on the UE. SS waits for the UE to send an initial REGISTER request, in accordance to 3GPP TS 24.229 [10], clause 5.1.1.2
5484: 2)	SS responds to the initial REGISTER request with an invalid 401 Unauthorized response, headers populated as follows:
5485: a)	To, From, Via, CSeq, Call-ID and Content-Length headers according to RFC 3261 [15] clauses 8.2.6.2 and 20.14; and
5486: b)	WWW-Authentication header with AKAv1-MD5 authentication challenge according to 3GPP TS 24.229 [10], clause 5.4.1.2.1 and RFC 3310 [17] clause 3; except that the MAC value in AUTN should be incorrect 
5487: c)	Security-Server header according to 3GPP TS 24.229 [10], clause 5.2.2 and RFC 3329 [21] clause 2.
5488: 3)	SS waits for the UE to send a second Registration message indicating that the received 401 Unauthorized message was invalid
5489: 4)	SS sends an invalid 401 Unauthorized message, same as in step 2)
5490: 5)	SS waits for the UE to send a third Registration message indicating that the received 401 Unauthorized message was invalid
5491: 6) - 12) SS completes the registration procedure (to get the UE in a stable state at the end of the test case).
5492: Expected sequence
5493: Step
5494: Direction
5495: Message
5496: Comment
5498: UE
5499: SS
5502: 1
5503: -->
5504: REGISTER
5505: UE sends initial registration for IMS services.
5506: 2
5507: <--
5508: 401 Unauthorized
5509: The SS responds with an invalid AKAv1-MD5 authentication challenge with an invalid MAC value.
5510: 3
5511: -->
5512: REGISTER
5513: REGISTER request:
5514: - contains no AUTS directive and an empty response directive, i.e. no authentication challenge response 
5515: - UE populates a new Security-Client header set to specify the security mechanism it supports, the IPsec layer algorithms it supports and the parameters needed for the new security association setup
5516: 4
5517: <--
5518: 401 Unauthorized
5519: The SS responds with an invalid AKAv1-MD5 authentication challenge with an invalid MAC value.
5520: 5
5521: -->
5522: REGISTER
5523: REGISTER request:
5524: - contains no AUTS directive and an empty response directive, i.e. no authentication challenge response
5525: - UE populates a new Security-Client header set to specify the security mechanism it supports, the IPsec layer algorithms it supports and the parameters needed for the new security association setup 
5526: 6
5527: <--
5528: 401 Unauthorized
5529: The SS responds with a valid AKAv1-MD5 authentication challenge and security mechanisms supported by the network.
5530: 7
5531: -->
5532: REGISTER
5533: UE completes the security negotiation procedures, sets up a temporary set of SAs and uses those for sending another REGISTER with AKAv1-MD5 credentials.
5534: 8
5535: <--
5536: 200 OK
5537: The SS responds with 200 OK.
5538: 9
5539: -->
5540: SUBSCRIBE
5541: UE subscribes to its registration event package. 
5542: 10
5543: <--
5544: 200 OK
5545: The SS responds SUBSCRIBE with 200 OK
5546: 11
5547: <--
5548: NOTIFY
5549: The SS sends initial NOTIFY for registration event package, containing full registration state information for the registered public user identity in the XML body 
5550: 12
5551: -->
5552: 200 OK
5553: The UE responds the NOTIFY with 200 OK
5555: Specific message contents
5556: REGISTER (Step 1)
5557: Use the default message "REGISTER" in annex A.1.1 with condition A1.
5558: 401 UNAUTHORIZED (Steps 2 and 4)
5559: Use the default message "401 Unauthorized for REGISTER" in annex A.1.2 with the following exceptions:
5560: Header/param
5561: Value/remark
5562: WWW-Authenticate
5564: 	nonce
5565: Base 64 encoding of RAND and AUTN, incorrect MAC value is used to generate
5567: REGISTER (Steps 3 and 5)
5568: Use the default message "REGISTER" in annex A.1.1 with condition A1 with the following exceptions:
5569: Header/param
5570: Value/remark
5571: CSeq
5573: 	value
5574: The value sent in the previous REGISTER message + 1 (incremented)
5575: Call-ID
5577: 	callid
5578: The same value as in REGISTER in Step 1
5579: Authorization
5581: 	response
5582: It shall be present but empty
5583: 	auth-param
5584: If present it shall not contain the auts directive
5585: 	nonce-count
5586: value or presence of the parameter not to be checked
5587: Security-Client
5589:      spi-c
5590: new SPI number of the inbound SA at the protected client port, must be different from the value used in step 1 (and step 3 when in step 5)
5591:      spi-s
5592: new SPI number of the inbound SA at the protected server port, must be different from the value used in step 1 (and step 3 when in step 5)
5593:      port-c
5594: new protected client port needed for the setup of new pairs of security associations, must be different from the value used in step 1 (and step 3 when in step 5)
5596: 9.1.5	Test requirements
5597: SS shall check in step 3 and 5 that in accordance to the 3GPP TS 24.229 [10] clause 5.1.1.5
5598: -	the UE responds with a further REGISTER indicating to the S-CSCF that the challenge has been deemed invalid; and
5599: -	sends the REGISTER request using no security associations; and
5600: -	the REGISTER request contains no AUTS directive and an empty response directive, i.e. no authentication challenge; and
5601: -	populates a new Security-Client header within the REGISTER request, set to specify the security mechanism it supports, the IPsec layer algorithms it supports and the parameters needed for the new security association setup; and
5602: -	does not create a temporary set of security associations.
```

## 9.2 Invalid Behaviour - SQN out of range（行 5603-5739；used_by: TC-013）

关键官方标记：`9.2.1	Definition`、`9.2.2	Conformance requirement`、`9.2.3	Test purpose`、`9.2.4	Method of test`、`9.2.5	Test requirements`、`SQN value in AUTN should be out of range`、`contains AUTS directive`、`auts= "auts-value"`、`temporary set of security associations`

> 原文差异保留：The 9.2 Test purpose text says no auts and an empty response, while the later step 3, Specific Message Contents and Test requirements explicitly require AUTS for the SQN-out-of-range case. This extraction preserves both source statements and does not rewrite either one.

```text
5603: 9.2	Invalid Behaviour - SQN out of range 
5604: 9.2.1	Definition
5605: To test that the UE when receiving a 401 (Unauthorized) response with SQN out of range to its initial REGISTER request behaves correctly. This procedure is described in 3GPP TS 24.229 [10] clause 5.1.1.5. 
5606: To test after a failed authentication attempt that the UE when receiving a valid 401 (Unauthorized) response to its initial REGISTER request behaves correctly. This procedure is described in 24.229 [10] clause 5.1.1.5.
5607: 9.2.2	Conformance requirement
5608: [TS 24.229, clause 5.1.1.5.1]
5609: Authentication is performed during initial registration. A UE can be re-authenticated during subsequent reregistrations, deregistrations or registrations of additional public user identities. When the network requires authentication or re-authentication of the UE, the UE will receive a 401 (Unauthorized) response to the REGISTER request.
5610: On receiving a 401 (Unauthorized) response to the REGISTER request, the UE shall:
5611: 1)	extract the RAND and AUTN parameters;
5612: 2)	check the validity of a received authentication challenge, as described in 3GPP TS 33.203 [19] i.e. the locally calculated XMAC must match the MAC parameter derived from the AUTN part of the challenge; and the SQN parameter derived from the AUTN part of the challenge must be within the correct range; and
5613: ...
5614: [TS 24.229 Rel-12, clause 5.1.1.5.3]
5615: If, in a 401 (Unauthorized) response, either the MAC or SQN is incorrect the UE shall respond with a further REGISTER indicating to the S-CSCF that the challenge has been deemed invalid as follows:
5616: -	in the case where the UE deems the MAC parameter to be invalid the subsequent REGISTER request shall contain no "auts" Authorization header field parameter and an empty "response" Authorization header field parameter, i.e. no authentication challenge response;
5617: -	in the case where the UE deems the SQN to be out of range, the subsequent REGISTER request shall contain the "auts" Authorization header field parameter (see 3GPP TS 33.102 [18]).
5618: NOTE:	In the case of the SQN being out of range, a "response" Authorization header field parameter can be included by the UE, based on the procedures described in RFC 3310 [49].
5619: Whenever the UE detects any of the above cases, the UE shall:
5620: -	send the REGISTER request using an existing set of security associations, if available (see 3GPP TS 33.203 [19]);
5621: -	populate a new Security-Client header field within the REGISTER request and associated contact address, set to specify the security mechanisms it supports, the IPsec layer algorithms for integrity and confidentiality protection it supports and the parameters needed for the new security association setup. These parameters shall contain new values for spi_uc, spi_us and port_uc; and 
5622: -	not create a temporary set of security associations.
5623: 9.2.3	Test purpose
5624: 1)	To verify that after receiving a 401 (Unauthorized) response for the initial REGISTER sent, the UE checks that the SQN parameter derived from the AUTN part of the authentication challenge is within the correct range.
5625: 2)	If the value of SQN derived from the AUTN part of the 401 (Unauthorized) received by the UE is out of range: 
5626: -	the UE responds with a further REGISTER indicating that the challenge has been deemed invalid; and
5627: -	this subsequent REGISTER request contains no "auts" Authorization header field parameter and an empty "response" Authorization header field parameter, i.e. no authentication challenge response; and
5628: -	the UE populates a new Security-Client header field within the REGISTER request and associated contact address, set to specify the security mechanism it supports, the IPsec layer algorithms it supports and the parameters needed for the new security association setup. These parameters contain new values for spi_uc, spi_us and port_uc; and
5629: -	the UE does not create a temporary set of security associations.
5630: 3)	To verify after a failed authentication attempt if the UE receives a valid 401 (Unauthorized) message from the network in response to the Register request sent, the UE is able to perform the authentication and registration successfully.
5631: 9.2.4	Method of test
5632: Initial conditions
5633: UE contains either ISIM and USIM applications or only USIM application on UICC. UE is not registered to IMS services, but has discovered the SS as P-CSCF by executing the generic test procedure in Annex C.2 up to step 3.
5634: SS is configured with the shared secret key of IMS AKA algorithm, related to the IMS private user identity (IMPI) configured on the UICC card equipped into the UE. SS is able to perform AKAv1-MD5 authentication algorithm for that IMPI, according to 3GPP TS 33.203 [14] clause 6.1 and RFC 3310 [17]. SS is listening to SIP default port 5060 for both UDP and TCP protocols.
5635: Test procedure
5636: 1)	IMS registration is initiated on the UE. SS waits for the UE to send an initial REGISTER request, in accordance to 3GPP TS 24.229 [10], clause 5.1.1.2
5637: 2)	SS responds to the initial REGISTER request with an invalid 401 Unauthorized response, headers populated as follows:
5638: a)	To, From, Via, CSeq, Call-ID and Content-Length headers according to RFC 3261 [15] clauses 8.2.6.2 and 20.14; and
5639: b)	WWW-Authentication header with AKAv1-MD5 authentication challenge according to 3GPP TS `24.229 [10], clause 5.4.1.2.1 and RFC 3310 [17] clause 3; except that the SQN value in AUTN should be out of range
5640: c)	Security-Server header according to 3GPP TS 24.229 [10], clause 5.2.2 and RFC 3329 [21] clause 2.
5641: 3)	SS waits for the UE to send a second Registration message indicating that the received 401 Unauthorized message was invalid
5642: 4)	SS sends a valid 401 Unauthorized message to the UE
5643: 5)	SS waits for the UE to send a Registration request using the temporary set of security associations to protect the message. The Registration request shall contain the valid answer to the authentication challenge in 401 Unauthorized sent in the previous step
5644: 6)	Continue test execution with the Generic test procedure in Annex C.2, step 7, sent over the same temporary set of security associations that the UE used for sending the REGISTER request
5645: Expected sequence
5646: Step
5647: Direction
5648: Message
5649: Comment
5651: UE
5652: SS
5655: 1
5656: -->
5657: REGISTER
5658: UE sends initial registration for IMS services.
5659: 2
5660: <--
5661: 401 Unauthorized
5662: The SS responds with an invalid AKAv1-MD5 authentication challenge with SQN out of range.
5663: 3
5664: -->
5665: REGISTER
5666: REGISTER request:
5667: - contains AUTS directive
5668: - UE populates a new Security-Client header set to specify the security mechanism it supports, the IPsec layer algorithms it supports and the parameters needed for the new security association setup.
5669: 4
5670: <--
5671: 401 Unauthorized
5672: This is a valid 401 (Unauthorized) message.
5673: 5
5674: -->
5675: REGISTER
5676: Message is sent using the temporary set of security associations to protect the message.
5677: Contains the valid answer to the authentication challenge sent in the 401 (Unauthorized) message.
5678: 6
5679: <---->
5680: Continue with Annex C.2 step 7
5681: Execute the Generic test procedure Annex C.2 steps 7-11 in order to get the UE in a stable registered state.
5683: Specific message contents
5684: REGISTER (Step 1)
5685: Use the default message "REGISTER" in annex A.1.1 with condition A1.
5686: 401 UNAUTHORIZED (Step 2)
5687: Use the default message "401 Unauthorized for REGISTER" in annex A.1.2 with the following exceptions:
5688: Header/param
5689: Value/remark
5690: WWW-Authenticate
5692: 	nonce
5693: Base 64 encoding of RAND and AUTN, generated with SQN out of range with the AMF information field set to AMFRESYNCH value to trigger SQN re-synchronisation procedure in test ISIM/USIM, see TS 34.108 clause 8.1.2.2.
5695: REGISTER (Step 3)
5696: Use the default message "REGISTER" in annex A.1.1 with condition A1 with the following exceptions:
5697: Header/param
5698: Value/remark
5699: CSeq
5701: 	value
5702: The value sent in the previous REGISTER message + 1 (incremented)
5703: Call-ID
5705: 	callid
5706: The same value as in REGISTER in Step 1
5707: Authorization
5709: 	nonce
5710: Same value as the opaque value in the previous 401 UNAUTHORIZED message
5711: 	opaque
5712: Same value as the opaque value in the previous 401 UNAUTHORIZED message
5713: 	response
5714: parameter may exist, but value not to be checked
5715: 	auth-param
5716: auts= "auts-value", auts-value not to be checked
5717: 	nonce-count
5718: value or presence of the parameter not to be checked
5719: Security-Client
5721:      spi-c
5722: new SPI number of the inbound SA at the protected client port, must be different from the value used in step 1
5723:      spi-s
5724: new SPI number of the inbound SA at the protected server port, must be different from the value used in step 1
5725:      port-c
5726: new protected client port needed for the setup of new pairs of security associations, must be different from the value used in step 1
5728: REGISTER (Step 5)
5729: Use the default message "REGISTER" in annex A.1.1 with condition A2.
5730: 9.2.5	Test requirements
5731: SS shall check in step 3 that in accordance to the 3GPP TS 24.229 [10] clause 5.1.1.5
5732: -	the UE responds with a further REGISTER indicating to the S-CSCF that the challenge has been deemed invalid; and
5733: -	sends the REGISTER request using no security associations; and
5734: -	the REGISTER request contains "auts" Authorization header field parameter; and
5735: -	populates a new Security-Client header within the REGISTER request, set to specify the security mechanism it supports, the IPsec layer algorithms it supports and the parameters needed for the new security association setup; and
5736: -	does not create a temporary set of security associations.
5737: SS shall check in step 5 that in accordance to the 3GPP TS 24.229 [10] clause 5.1.1.5
5738: -	the UE sets up the temporary set of security associations between the ports announced in Security-Client header (UE) in the REGISTER request and Security-Server header (SS) in the 401 Unauthorized response; and
5739: -	sends the Registration request using the temporary set of security associations to protect the message.
```

## 10.1 Invalid Behaviour - 503 Service Unavailable（行 5741-5809；used_by: TC-032）

关键官方标记：`10.1.1	Definition`、`10.1.2	Conformance requirement`、`10.1.3	Test purpose`、`10.1.4	Method of test`、`10.1.5	Test requirements`、`503 Service Unavailable`、`Retry-After`、`shall not automatically reattempt`、`SUBSCRIBE`

```text
5741: 10.1	Invalid Behaviour - 503 Service Unavailable
5742: 10.1.1	Definition
5743: Test to verify that when the UE receives a 503 (Service Unavailable) response to a SUBSCRIBE request containing a Retry-After header, then the UE shall not automatically reattempt the request until after the period indicated by the Retry-After header contents. This can happen when the server is temporarily unable to process the request due to a temporary overloading or maintenance of the server. 
5744: 10.1.2	Conformance requirement
5745: [TS 24.229, clause 5.1.2.2]
5746: If the UA receives a 503 (Service Unavailable) response to an initial SUBSCRIBE request containing a Retry-After header, then the UE shall not automatically reattempt the request until after the period indicated by the Retry-After header contents.
5747: Reference(s)
5748: 3GPP TS 24.229 [10], clause 5.1.2.2.
5749: 10.1.3	Test purpose
5750: To verify that after receiving a 503 (Service Unavailable) response to a SUBSCRIBE request, containing a Retry-After header, the UE shall not automatically reattempt the request until after the period indicated by the Retry-After header contents. This can happen when the server is temporarily unable to process the request due to a temporary overloading or maintenance of the server.
5751: 10.1.4	Method of test
5752: Initial conditions
5753: UE contains either ISIM and USIM applications or only USIM application on UICC. UE has activated a PDP context, discovered P-CSCF and registered to IMS services, by executing the generic test procedure in Annex C.2 up to step 7 or C.2a (GIBA only) up to step 5.
5754: SS is configured with the shared secret key of IMS AKA algorithm, related to the IMS private user identity (IMPI) configured on the UICC card equipped into the UE. SS has performed AKAv1-MD5 authentication with the UE and accepted the registration (IMS security).
5755: Test procedure
5756: 1)	The UE sends a SUBSCRIBE request over the established security associations.
5757: 2)	The SS responds to the SUBSCRIBE request with a 503 (Service Unavailable) response with the Retry-After header with period set to T, indicating how long the service is expected to be unavailable to the requesting client.
5758: 3)	The SS waits for the period of time T defined in the Retry-After header, to check that the UE does not try to SUBSCRIBE for the registration event during this period.
5759: 4)	The UE sends a new SUBSCRIBE request.
5760: 5)	Continue test execution with the Generic test procedure in Annex C.2 or C.2a (GIBA only), step 9.
5761: Expected sequence
5762: Step
5763: Direction
5764: Message
5765: Comment
5767: UE
5768: SS
5771: 1
5772: -->
5773: SUBSCRIBE
5774: UE subscribes to its registration event package. 
5775: 2
5776: <--
5777: 503 Service Unavailable
5778: The SS responds with 503 response containing a Retry-After header with period set to T.
5779: 3
5782: SS waits for Time T to check that the UE does not re-attempt the request.
5783: 4
5784: -->
5785: SUBSCRIBE 
5786: UE reattempts to subscribe to its registration event package.
5787: 5
5788: <---->
5789: Continue with Annex C.2 step 9
5790: Execute the Generic test procedure Annex C.2 steps 9-11 in order to get the UE in a stable registered state.
5792: NOTE:	The default messages contents in annex A are used with condition "IMS security " or "GIBA" when applicable
5793: Specific Message Contents
5794: SUBSCRIBE (Step 1)
5795: Use the default message "SUBSCRIBE for reg-event package" in annex A.1.4.
5796: 503 Service Unavailable response (Step 2)
5797: Use the default message "503 Service Unavailable" in annex A.4.2.
5798: SUBSCRIBE (Step 4)
5799: Use the default message "SUBSCRIBE for reg-event package" in annex A.1.4 with the following exception:
5800: Header/param
5801: Value/remark
5802: Call-ID
5804: 	callid
5805: value different from the previous SUBSCRIBE request
5807: 10.1.5	Test requirements
5808: Step 3: The UE shall not automatically reattempt the request during the period duration T.
5809: Step 4: The UE reattempts to send a SUBSCRIBE request for registration event package.
```

## 12.2 MO Call - 503 Service Unavailable（行 6060-6118；used_by: TC-032）

关键官方标记：`12.2.1	Definition`、`12.2.2	Conformance requirement`、`12.2.3	Test purpose`、`12.2.4	Method of test`、`12.2.5	Test requirements`、`503 Service Unavailable`、`Retry-After`、`ACK`、`INVITE`

```text
6060: 12.2	MO Call - 503 Service Unavailable
6061: 12.2.1	Definition
6062: When a server is temporarily unable to process an INVITE request due to a temporary overloading or maintenance of the server sends a 503 Service Unavailable response. The server may indicate when the service will be available again in a Retry-After header field. This process is described in 3GPP TS 24.229 [10], clause 5.1.3.1. 
6063: 12.2.2	Conformance requirement
6064: Upon receiving a 503 (Service Unavailable) response to an initial INVITE request containing a Retry-After header, then the originating UE shall not automatically reattempt the request until after the period indicated by the Retry-After header contents.
6065: Reference(s)
6066: 3GPP TS 24.229 [10], clause 5.1.3.1.
6067: 12.2.3	Test purpose
6068: To verify that when the UE receives a 503 (Service Unavailable) response to an initial INVITE request containing a Retry-After header, then the UE shall not automatically reattempt the request until after the period indicated by the Retry-After header contents.
6069: 12.2.4	Method of test
6070: Initial conditions
6071: UE contains either ISIM and USIM applications or only USIM application on UICC. UE has discovered P-CSCF and registered to IMS services, by executing the generic test procedure in Annex C.2 or C.2a (GIBA only) up to the last step.
6072: SS is configured with the shared secret key of IMS AKA algorithm, related to the IMS private user identity (IMPI) configured on the UICC card equipped into the UE. SS has performed AKAv1-MD5 authentication with the UE and accepted the registration (IMS security).
6073: Test procedure applicable for a UE with E-UTRA support (TS 34.229-2 [5] A.18/1)
6074: For value of T see specific message content for 503 (Service Unavailable) message.
6075: 1-8)	UE executes the procedures described in TS 36.508 [94] table 4.5A.6.3-1 steps 1 to 8.
6076: 9)	The SS responds with a 503 (Service Unavailable) response with the Retry-After header set to T.
6077: 10)	The SS waits for the UE to send an ACK to acknowledge the reception of the 503 (Service Unavailable) response.
6078: 11)	SS waits for a duration of time T and checks that the UE does not reattempt sending the INVITE request. After the time T the UE may reattempt sending the INVITE request.
6079: 12)	The UE may reattempt sending the INVITE request after time T.
6080: Expected sequence
6081: NOTE:	Only the IMS procedure relevant to the test purpose is described below.
6082: Step
6083: Direction
6084: Message
6085: Comment
6087: UE
6088: SS
6091: 1-3
6093: Steps 1, 2 and 3 defined in annex C.21
6094: MTSI MO speech call. Referred from 36.508 [94] table 4.5A.6.3-1 for a UE with E-UTRA support.
6095: 4
6096: <--
6097: 503 Service Unavailable
6098: Including Retry-After header with period set to T
6099: 5
6100: -->
6101: ACK
6102: The UE acknowledges the reception of the 503 (Service Unavailable) response
6103: 6
6106: The SS waits for a duration of time T and checks that the UE does not re-send the INVITE request
6107: 7
6109: Step 2 defined in annex C.21
6110: Optional
6112: NOTE:	The default messages contents in annex A are used with condition "IMS security" or "GIBA" when applicable
6113: Specific Message Contents
6114: Steps 1 - 3 as specified in annex C.21
6115: 503 Service Unavailable (Step 4)
6116: Use the default message "503 Service Unavailable" in annex A.4.2.
6117: 12.2.5	Test requirements
6118: At step 6 the UE shall not reattempt the INVITE request before time T from the time the SS receives the ACK from the UE in step 5.
```

## 12.2a MO Call - 504 Server Time-out（行 6119-6186；used_by: TC-015, TC-032）

关键官方标记：`12.2a.1	Definition`、`12.2a.2	Conformance requirement`、`12.2a.3	Test purpose`、`12.2a.4	Method of test`、`12.2a.5	Test requirements`、`504 Server Time-out`、`P-Asserted-Identity`、`initial registration`、`Service-Route`

```text
6119: 12.2a	MO Call - 504 Server Time-out
6120: 12.2a.1	Definition
6121: When the S-CSCF is temporarily unable to process an INVITE as the S-CSCF does not have the user profile or does not trust the data that it has (e.g. due to restart), the S-CSCF can reject the request by returning a 504 (Server Time-out) response to the UE with specific content as specified in 3GPP TS 24.229 [10] clause 5.4.3.2. As a result the UE will initiate restoration procedures by performing an initial registration.
6122: 12.2a.2	Conformance requirement
6123: In the event the UE receives a 504 (Server Time-out) response containing:
6124: 1)	a P-Asserted-Identity header field set to a value equal to a URI:
6125: a)	from the Service-Route header field value received during registration; or
6126: b)	from the Path header field value received during registration; and
6127: 2)	a Content-Type header field set according to subclause 7.6 (i.e. "application/3gpp-ims+xml"), independent of the value or presence of the Content-Disposition header field, independent of the value or presence of Content-Disposition parameters, then the default content disposition, identified as "3gpp-alternative-service", is applied as follows:
6128: a)	if the 504 (Server Time-out) response includes an IM CN subsystem XML body as described in subclause 7.6 with the <ims-3gpp> element, including a version attribute, with the <alternative-service> child element:
6129: a)	with the <type> child element set to "restoration" (see table 7.7AA); and
6130: b)	with the <action> child element set to "initial-registration" (see table 7.7AB);
6131: 	then the UE:
6132: -	shall initiate restoration procedures by performing an initial registration as specified in subclause 5.1.1.2; and
6133: -	may provide an indication to the user based on the text string contained in the <reason> child element of the <alternative-service> child element of the <ims-3gpp> element.
6134: Reference(s)
6135: 3GPP TS 24.229 [10], clause 5.1.2A.1.6
6136: 12.2a.3	Test purpose
6137: To verify that when the UE receives a 504 (Server Time-out) response to an INVITE request containing a P-Asserted-Identity header field set to a value equal to a URI from the Service-Route header field value received during registration and the rest of the message is set as described in [10] subclause 5.1.2A.1.6, then the UE initiates restoration procedures by performing an initial registration as specified in [10] subclause 5.1.1.2.
6138: 12.2a.4	Method of test
6139: Initial conditions
6140: UE contains an ISIM and USIM or only USIM application on the UICC. UE has activated a PDP context/EPS bearer, discovered P-CSCF and registered to IMS services, by executing the generic test procedure in Annex C.2 up to the last step.
6141: SS is configured with the shared secret key of IMS AKA algorithm, related to the IMS private user identity (IMPI) configured on the UICC card equipped into the UE. SS has performed AKAv1-MD5 authentication with the UE and accepted the registration (IMS security).
6142: Test procedure applicable for a UE with E-UTRA support (TS 34.229-2 [5] A.18/1)
6143: 1-8)	UE executes the procedures described in TS 36.508 [94] table 4.5A.6.3-1 steps 1 to 8.
6144: 9)	The SS responds with a 504 (Server Time-out) response. 
6145: 10)	The SS waits for the UE to send an ACK to acknowledge the reception of 504 (Server Time-out) response.
6146: 11-18)	As specified in steps 4-11 annex C.2.
6147: Expected sequence
6148: NOTE:	Only the IMS procedure relevant to the test purpose is described below.
6149: Step
6150: Direction
6151: Message
6152: Comment
6154: UE
6155: SS
6158: 1-2
6160: Steps 1-2 defined in annex C.21
6161: MTSI MO speech call. Referred from 36.508 [94] table 4.5A.6.3-1 for a UE with E-UTRA support.
6162: 3
6163: <--
6164: 504 Server Time-out
6165: Set as per the specific message contents.
6166: 4
6167: -->
6168: ACK
6170: 5-12
6171: -->
6172: Steps 4-11 defined in annex C.2
6173: The UE performs an initial registration.
6175: NOTE:	The default messages contents in annex A are used with condition "IMS security" or "GIBA" when applicable.
6176: Specific Message Contents
6177: Steps 1-2
6178: As specified in annex C.21
6179: 504 Server Time-out (Step 3)
6180: Use the default message "504 Server Time-out" in Annex A.4.6
6181: ACK (Step 4)
6182: As specified in annex A.2.7.
6183: Steps 5-12
6184: As specified in annex C.2.
6185: 12.2a.5	Test requirements
6186: After step 3 the UE shall perform an initial registration.
```

> 状态：这些是官方 TP 原文骨架。正式 P/F 仍只能由 SS/一致性仪表按对应 `34.229-1` 条目执行产生。

REGISTER sip:ims.example.com SIP/2.0
Via: SIP/2.0/UDP 192.0.2.10:5060;branch=z9hG4bK-mock-mac-1;rport
From: <sip:alice@ims.example.com>;tag=abc
To: <sip:alice@ims.example.com>
Call-ID: mock-tc13-mac-0001
CSeq: 1 REGISTER
Contact: <sip:alice@192.0.2.10:5060>;ob
Expires: 300
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=1000; spi-s=1001; port-c=5001; port-s=5002

SIP/2.0 401 Unauthorized
Via: SIP/2.0/UDP 192.0.2.10:5060;branch=z9hG4bK-mock-mac-1;rport
From: <sip:alice@ims.example.com>;tag=abc
To: <sip:alice@ims.example.com>;tag=ss-1
Call-ID: mock-tc13-mac-0001
CSeq: 1 REGISTER
WWW-Authenticate: Digest realm="ims.example.com", nonce="mock-invalid-mac-nonce", algorithm=AKAv1-MD5, opaque="op-1", qop="auth,auth-int", ck="ck", ik="ik"
Security-Server: ipsec-3gpp; alg=hmac-md5-96; spi-c=2000; spi-s=2001; port-c=6001; port-s=6002

REGISTER sip:ims.example.com SIP/2.0
Via: SIP/2.0/UDP 192.0.2.10:5060;branch=z9hG4bK-mock-mac-2;rport
From: <sip:alice@ims.example.com>;tag=abc
To: <sip:alice@ims.example.com>
Call-ID: mock-tc13-mac-0001
CSeq: 2 REGISTER
Contact: <sip:alice@192.0.2.10:5060>;ob
Expires: 300
Authorization: Digest username="alice@ims.example.com", realm="ims.example.com", nonce="mock-invalid-mac-nonce", uri="sip:ims.example.com", response="", algorithm=AKAv1-MD5, opaque="op-1"
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=1002; spi-s=1003; port-c=5003; port-s=5004

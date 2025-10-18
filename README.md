PySendFax is based on [faxmail](https://github.com/kkajita/faxmail)   
## Requirements   
+ Asterisk
+ python bottle
+ ImageMagick
+ Ghostscript
## Run
```
pysendfax/uploder.py 0.0.0.0 8080 <TRUNK> <CONTEXT>
```
browse
```
http://localhost:8080
```
## Sample extensions.conf
```
general]
static=yes
writeprotect=no
clearglobalvars=no

[globals]
HEADERINFO=Foo Bar
LOCALSTATIONID=050-xxxx-xxxx
TOADDR=foo@gmail.com
SENDMAIL=/usr/local/bin/sendmail.py
FROMADDR=Fax Agent <${TOADDR}>

[default]

[plala-context]
exten => s,1,NoOp(${EXTEN})
same => n,Answer
same => n,Playback(hello)
same => n,Playback(hello)
same => n,Playback(hello)
same => n,Playback(hello)
same => n,Playback(hello)
same => n,Hangup

exten => fax,1,NoOp(Faxin-${EXTEN})
same => n,Goto(rec-fax,receive,1)

[rec-fax]
exten => receive,1,NoOp(Faxin-${EXTEN})
same => n,Set(FAXOPT(maxrate)=4800)
same => n,Set(FAXOPT(minrate)=2400)
same => n,Set(FAXOPT(modem)=v17,v27,v29)
same => n,Set(FAXFILE=/var/spool/asterisk/${EPOCH}.incoming.tiff)
same => n,ReceiveFAX(${FAXFILE})
same => n,Hangup


; Hangup.
exten => h,1,NoOp(rec-fax: Hangup )
same => n,NoOp(FAX Status: ${FAXSTATUS})
same => n,GotoIf($["${FAXSTATUS}" != "SUCCESS"]?failed)
same => n,NoOp(FAXOPT(ecm): ${FAXOPT(ecm)})
same => n,NoOp(FAXOPT(filename): ${FAXOPT(filename)})
same => n,NoOp(FAXOPT(headerinfo): ${FAXOPT(headerinfo)})
same => n,NoOp(FAXOPT(localstationid): ${FAXOPT(localstationid)})
same => n,NoOp(FAXOPT(maxrate): ${FAXOPT(maxrate)})
same => n,NoOp(FAXOPT(minrate): ${FAXOPT(minrate)})
same => n,NoOp(FAXOPT(pages): ${FAXOPT(pages)})
same => n,NoOp(FAXOPT(rate): ${FAXOPT(rate)})
same => n,NoOp(FAXOPT(remotestationid): ${FAXOPT(remotestationid)})
same => n,NoOp(FAXOPT(resolution): ${FAXOPT(resolution)})
same => n,NoOp(FAXOPT(faxdetect): ${FAXOPT(faxdetect)})
same => n,NoOp(FAXOPT(status): ${FAXOPT(status)})
same => n,NoOp(FAXOPT(statusstr): ${FAXOPT(statusstr)})
same => n,NoOp(FAXOPT(error): ${FAXOPT(error)})
same => n,System(${SENDMAIL} "${TOADDR}" -f "${FROMADDR}" -a ${FAXFILE} -s "Fax Received from ${CALLERID(num)}")
same => n,Hangup
same => n(failed),System(${SENDMAIL} "${TOADDR}" -f "${FROMADDR}" -a ${FAXFILE} -s "[FAILED] Fax Received from ${CALLERID(num)}" -b "STATUS: ${FAXSTATUS}\nERROR: ${FAXERROR}\n\n")

[send-fax]
exten => send,1,NoOp(Faxout-${EXTEN}: FAXFILE=${FAXFILE})
same => n,Set(FAXOPT(headerinfo)=${HEADERINFO})
same => n,Set(FAXOPT(localstationid)=${LOCALSTATIONID})
same => n,Set(FAXOPT(maxrate)=4800)
same => n,Set(FAXOPT(minrate)=2400)
same => n,SendFax(${FAXFILE},d)
same => n,Hangup

exten => failed,1,Set(FAXSTATUS=DIALFAIL)
same => n,Set(FAXERROR=No Answer)
same => n,Set(FAXPAGES=0)
same => n,Hangup

exten => h,1,NoOP(*** SEND FAX FINISHED: STATUS=${FAXSTATUS} ***)
same => n,GotoIf($["${FAXSTATUS}" != "SUCCESS"]?failed)
same => n,NoOp(FAXOPT(status): ${FAXOPT(status)})
same => n,NoOp(FAXOPT(statusstr): ${FAXOPT(statusstr)})
same => n,NoOp(FAXOPT(error): ${FAXOPT(error)})
same => n,System(${SENDMAIL} "${REPLYTO}" -a "${FAXFILE}" -f "${FROMADDR}" -s "${SUBJECT}" -b "FAXNUMBER: ${FAXNUMBER}\nSTATUS: ${FAXSTATUS}\nPAGES: ${FAXPAGES}\nBITRATE: ${FAXBITRATE}\nRESOLUTION: ${FAXRESOLUTION}\n\n")
same => n,Hangup
same => n(failed),System(${SENDMAIL} "${REPLYTO}" -a "${FAXFILE}" -f "${FROMADDR}" -s "[FAILED] ${SUBJECT}" -b "FAXNUMBER: ${FAXNUMBER}\nSTATUS: ${FAXSTATUS}\nERROR: ${FAXERROR}\n\n")
same => n,NoOp(SEND FAX FAIL)
same => n,NoOp(FAXSTATUS: ${FAXSTATUS})
same => n,NoOp(FAXERROR: ${FAXERROR})

```
This case's \<CONTEXT\> is 'send-fax'.   

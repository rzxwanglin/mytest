UTF8Length = function f(a) {
    var b = 0;
    for (var c = 0, d = a.length; c < d; c++) {
        var e = a.charCodeAt(c);
        e < 128 ? b += 1 : e < 2048 ? b += 2 : e >= 55296 && e <= 56319 ? (b += 4,
        c++) : b += 3
    }
    return b
}
convertStringToUTF8 = function j(a, b, c) {
    c = c;
    for (var d = 0, e = a.length; d < e; d++) {
        var f = a.charCodeAt(d);
        f < 128 ? b[c++] = f : f < 2048 ? (b[c++] = 192 | f >> 6,
        b[c++] = 128 | f & 63) : f < 55296 || f >= 57344 ? (b[c++] = 224 | f >> 12,
        b[c++] = 128 | f >> 6 & 63,
        b[c++] = 128 | f & 63) : (f = 65536 + ((f & 1023) << 10 | a.charCodeAt(++d) & 1023),
        b[c++] = 240 | f >> 18,
        b[c++] = 128 | f >> 12 & 63,
        b[c++] = 128 | f >> 6 & 63,
        b[c++] = 128 | f & 63)
    }
}
a_=  function a(a, b) {
            this.payloadString = a,
            this.payloadBytes = b
        }

create = function(b) {
    var c = new Uint8Array(new ArrayBuffer(UTF8Length(b)));
    convertStringToUTF8(b, c, 0);
    return new a_(b,c)
} 


coinflip = function b(b) {
                return a.apply(this, arguments)
            }
scheduleLoggingCallback= function(a) {
            return this.$9 != null ? this.$9(a) : a()
        }

b = function a(a) {
            h ={
              "CONNECT": 1,
              "CONNACK": 2,
              "PUBLISH": 3,
              "PUBACK": 4,
              "SUBSCRIBE": 8,
              "SUBACK": 9,
              "UNSUBSCRIBE": 10,
              "UNSUBACK": 11,
              "PINGREQ": 12,
              "PINGRESP": 13,
              "DISCONNECT": 14
          }
            this.messageType = h[a]
}
Publish = function a(a, c, d, e, f, g) {
            var h;
            h = b.call(this, "PUBLISH") || this;
            h.topic = a;
            h.payloadMessage = c;
            h.qos = d;
            h.messageIdentifier = e;
            h.retained = f != null ? f : !1;
            h.duplicate = g != null ? g : !1;
            if (h.qos === 1 && h.messageIdentifier == null)
                throw new TypeError("Argument Invalid. messageIdentifier: null and qos: 1");
            return h
}
cc =function() {
            var a = (this.messageType & 15) << 4;
            this.duplicate && (a |= 8);
            a = a |= this.qos << 1;
            this.retained && a != 1;
            var b = d("MqttProtocolUtils").UTF8Length(this.topic)
              , c = b + 2
              , e = this.qos === 0 ? 0 : 2;
            c += e;
            e = this.payloadMessage.bytes();
            c += e.byteLength;
            var f = d("MqttProtocolUtils").encodeMultiByteInt(c);
            c = new ArrayBuffer(1 + f.length + c);
            var g = new Uint8Array(c);
            g[0] = a;
            g.set(f, 1);
            a = 1 + f.length;
            a = d("MqttProtocolUtils").writeString(this.topic, b, g, a);
            this.qos !== 0 && this.messageIdentifier != null && (a = d("MqttProtocolUtils").writeUInt16BE(this.messageIdentifier, g, a));
            g.set(e, a);
            return c
}
mysend_ = function(a, b, c) {
  var e = 26
  a = new (Publish)(a,b,c,e);
  
  return a.encode()
}

var message  ='{"app_id":"936619743392459","payload":"{\\"epoch_id\\":7216452514390349329,\\"tasks\\":[{\\"failure_count\\":null,\\"label\\":\\"46\\",\\"payload\\":\\"{\\\\\\"thread_id\\\\\\":17846712582227458,\\\\\\"otid\\\\\\":\\\\\\"7216452496738747468\\\\\\",\\\\\\"source\\\\\\":65537,\\\\\\"send_type\\\\\\":1,\\\\\\"sync_group\\\\\\":1,\\\\\\"mark_thread_read\\\\\\":1,\\\\\\"text\\\\\\":\\\\\\"9999\\\\\\",\\\\\\"initiating_source\\\\\\":1,\\\\\\"skip_url_preview_gen\\\\\\":0,\\\\\\"text_has_links\\\\\\":0,\\\\\\"multitab_env\\\\\\":0}\\",\\"queue_name\\":\\"17846712582227458\\",\\"task_id\\":15},{\\"failure_count\\":null,\\"label\\":\\"21\\",\\"payload\\":\\"{\\\\\\"thread_id\\\\\\":17846712582227458,\\\\\\"last_read_watermark_ts\\\\\\":1720536350426,\\\\\\"sync_group\\\\\\":1}\\",\\"queue_name\\":\\"17846712582227458\\",\\"task_id\\":16}],\\"version_id\\":\\"8131648726891283\\",\\"data_trace_id\\":\\"#yfZEopN/TNGUNOk0DoQXYQ\\"}","request_id":33,"type":3}'
var message_ = create(message)

var ins = mysend_('/ls_req',message_,1)
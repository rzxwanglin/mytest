var h = {
        CONNECT: 1,
        CONNACK: 2,
        PUBLISH: 3,
        PUBACK: 4,
        SUBSCRIBE: 8,
        SUBACK: 9,
        UNSUBSCRIBE: 10,
        UNSUBACK: 11,
        PINGREQ: 12,
        PINGRESP: 13,
        DISCONNECT: 14
    }
var i = [0, 6, 77, 81, 73, 115, 100, 112, 3];

decodeMultiByteInt = function b(a, b) {
        b = b;
        var c = 0, d = 1, e;
        do {
            if (b === a.length)
                return null;
            e = a[b++];
            c += (e & 127) * d;
            d *= 128
        } while ((e & 128) !== 0);
        return {
            offset: b,
            value: c
        }
    }
readUInt16BE=  function b(a, b) {
        b = b;
        var c = 0, d = 1, e;
        do {
            if (b === a.length)
                return null;
            e = a[b++];
            c += (e & 127) * d;
            d *= 128
        } while ((e & 128) !== 0);
        return {
            offset: b,
            value: c
        }
    }

convertUTF8ToString =function k(a, b, c) {
        var d = []
          , e = b
          , f = 0;
        while (e < b + c) {
            var g = a[e++];
            if (g < 128)
                d[f++] = String.fromCharCode(g);
            else if (g > 191 && g < 224) {
                var h = a[e++];
                d[f++] = String.fromCharCode((g & 31) << 6 | h & 63)
            } else if (g > 239 && g < 365) {
                h = a[e++];
                var i = a[e++]
                  , j = a[e++];
                h = ((g & 7) << 18 | (h & 63) << 12 | (i & 63) << 6 | j & 63) - 65536;
                d[f++] = String.fromCharCode(55296 + (h >> 10));
                d[f++] = String.fromCharCode(56320 + (h & 1023))
            } else {
                i = a[e++];
                j = a[e++];
                d[f++] = String.fromCharCode((g & 15) << 12 | (i & 63) << 6 | j & 63)
            }
        }
        return d.join("")
    }
function a_(a, b) {
            this.payloadString = a,
            this.payloadBytes = b
        }
createWithBytes = function(b) {

            var c = convertUTF8ToString(b, 0, b.length);
            return new a_(c,b)
}

readUInt16BE = function e(a, b) {
        return 256 * a[b] + a[b + 1]
    }
function call_(a) {
            this.messageType = h[a]
}
q_=function a(a, c, d, e, f, g) {
            var h;
            h = call_("PUBLISH") || this;
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
function j(a, b) {
        b = b;
        var e = b
          , f = a[b]
          , g = f >> 4;
        b += 1;
        var i = decodeMultiByteInt(a, b);
        if (i == null)
            return {
                position: e,
                wireMessage: null
            };
        b = i.offset;
        i = b + i.value;
        if (i > a.length)
            return {
                position: e,
                wireMessage: null
            };
        var j;
        switch (g) {
        case h.CONNACK:
            e = a[b++];
            e = !!(e & 1);
            var o = a[b++];
            j = new m(e,o);
            break;
        case h.PUBLISH:
            e = f & 15;
            o = e >> 1 & 3;
            f = readUInt16BE(a, b);
            b += 2;
            var r = convertUTF8ToString(a, b, f);
            b += f;
            f = null;
            o === 1 && (f =readUInt16BE(a, b),
            b += 2);
            var s = createWithBytes(a.subarray(b, i))
              , t = (e & 1) === 1;
            e = (e & 8) === 8;
            j = new q_(r,s,o,f,t,e);
            break;
        case h.PINGREQ:
            function k_(a) {
                return call_(a) || this
            }
            j = new k_("PINGREQ");
            break;
        case h.PINGRESP:
            function k_(a) {
                return call_(a) || this
            }
            j = new k_("PINGRESP");
            break;
        case h.PUBACK:
        case h.UNSUBACK:
            function n_(a, c) {
                a = call_(a) || this;
                a.messageIdentifier = c;
                return a
            }
            r = readUInt16BE(a, b);
            j = new n_(g === h.PUBACK ? "PUBACK" : "UNSUBACK",r);
            break;
        case h.SUBACK:
            function l_(a, c) {
                var d;
                d = call_("SUBACK") || this;
                d.messageIdentifier = a;
                d.returnCode = c;
                return d
            }
            s = readUInt16BE(a, b);
            b += 2;
            o = a.subarray(b, i);
            j = new l_(s,o);
            break;
        default:

        }
        return {
            position: i,
            wireMessage: j
        }
    }

decodeByteMessages = function (a) {
       a = new Uint8Array(a)
        var b = []
          , c = 0;
        while (c < a.length) {
            var d = j(a, c)
              , e = d.wireMessage;
            c = d.position;
            if (e)
                b.push(e);
            else
                break
        }
        d = null;
        c < a.length && (d = a.subarray(c));
        return {
            messages: b,
            remaining: d
        }
    }
//
// a =decodeByteMessages([49, 238, 3, 0, 8, 47, 108, 115, 95, 114, 101, 115, 112, 123, 34, 114, 101, 113, 117, 101, 115, 116, 95, 105, 100, 34, 58, 54, 44, 34, 112, 97, 121, 108, 111, 97, 100, 34, 58, 34, 123, 92, 34, 110, 97, 109, 101, 92, 34, 58, 110, 117, 108, 108, 44, 92, 34, 115, 116, 101, 112, 92, 34, 58, 91, 49, 44, 91, 49, 44, 91, 52, 44, 48, 44, 49, 44, 91, 53, 44, 92, 34, 101, 120, 101, 99, 117, 116, 101, 70, 105, 114, 115, 116, 66, 108, 111, 99, 107, 70, 111, 114, 83, 121, 110, 99, 84, 114, 97, 110, 115, 97, 99, 116, 105, 111, 110, 92, 34, 44, 91, 49, 57, 44, 92, 34, 49, 92, 34, 93, 44, 91, 49, 57, 44, 92, 34, 55, 50, 49, 55, 56, 54, 51, 50, 56, 51, 50, 54, 54, 52, 55, 52, 53, 50, 57, 92, 34, 93, 44, 92, 34, 72, 67, 119, 82, 65, 65, 65, 87, 110, 65, 81, 87, 105, 73, 79, 75, 106, 65, 48, 84, 66, 82, 98, 117, 49, 77, 110, 90, 122, 52, 45, 48, 80, 119, 65, 92, 34, 44, 92, 34, 72, 68, 119, 87, 65, 82, 89, 66, 65, 65, 65, 87, 65, 82, 89, 66, 69, 119, 85, 87, 55, 116, 84, 74, 50, 99, 45, 80, 116, 68, 56, 65, 92, 34, 44, 91, 49, 57, 44, 92, 34, 51, 92, 34, 93, 44, 116, 114, 117, 101, 44, 91, 49, 57, 44, 92, 34, 48, 92, 34, 93, 44, 102, 97, 108, 115, 101, 44, 91, 49, 57, 44, 92, 34, 50, 92, 34, 93, 44, 91, 57, 93, 93, 93, 44, 91, 50, 51, 44, 91, 50, 44, 48, 93, 44, 91, 49, 93, 93, 93, 44, 91, 49, 44, 91, 53, 44, 92, 34, 101, 120, 101, 99, 117, 116, 101, 70, 105, 110, 97, 108, 108, 121, 66, 108, 111, 99, 107, 70, 111, 114, 83, 121, 110, 99, 84, 114, 97, 110, 115, 97, 99, 116, 105, 111, 110, 92, 34, 44, 116, 114, 117, 101, 44, 91, 49, 57, 44, 92, 34, 49, 92, 34, 93, 44, 91, 49, 57, 44, 92, 34, 55, 50, 49, 55, 56, 54, 51, 50, 56, 51, 50, 54, 54, 52, 55, 52, 53, 50, 57, 92, 34, 93, 93, 93, 93, 125, 34, 44, 34, 115, 112, 34, 58, 91, 34, 101, 120, 101, 99, 117, 116, 101, 70, 105, 114, 115, 116, 66, 108, 111, 99, 107, 70, 111, 114, 83, 121, 110, 99, 84, 114, 97, 110, 115, 97, 99, 116, 105, 111, 110, 34, 44, 34, 101, 120, 101, 99, 117, 116, 101, 70, 105, 110, 97, 108, 108, 121, 66, 108, 111, 99, 107, 70, 111, 114, 83, 121, 110, 99, 84, 114, 97, 110, 115, 97, 99, 116, 105, 111, 110, 34, 93, 44, 34, 116, 97, 114, 103, 101, 116, 34, 58, 51, 125])
// console.log(a)
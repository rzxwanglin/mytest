	
function writeUInt16BE(a, b, c) {
        c = c;
        b[c++] = a >> 8;
        b[c++] = a % 256;
        return c
    }
	

writeString=   function i(a, b, c, d) {
        function h(a, b, c) {
            c = c;
            b[c++] = a >> 8;
            b[c++] = a % 256;
            return c
        }
        function j(a, b, c) {
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
        d = h(b, c, d);
        j(a, c, d);
        return d + b
    }
	
function UTF8Length(a) {
        var b = 0;
        for (var c = 0, d = a.length; c < d; c++) {
            var e = a.charCodeAt(c);
            e < 128 ? b += 1 : e < 2048 ? b += 2 : e >= 55296 && e <= 56319 ? (b += 4,
            c++) : b += 3
        }
        return b
    }
	

	 


encode = function(mythis) {
			var i =[0, 6, 77, 81, 73, 115, 100, 112, 3]
            a = undefined, b = 16, c = 12
            //c =433
            c += UTF8Length(mythis.clientId) + 2;
            c += UTF8Length(mythis.connectOptions.userName) + 2;
            var e = [177, 3];
            c = new ArrayBuffer(436);
            var f = new Uint8Array(c);
            f[0] = b;   
            b = 1;
            f.set(e, 1);
            b += e.length;
            f.set(i, b);
            b += i.length;
            e = 2 | 128;
            f[b++] = e;
            b = writeUInt16BE(15, f, b);
            b = writeString("mqttwsclient",UTF8Length("mqttwsclient"), f, b);
            b = writeString(mythis.connectOptions.userName, UTF8Length(mythis.connectOptions.userName), f, b);
            return c
 }



Connect = function (b, c) {
            var d ={};
            d.messageType = 1
            d.clientId = 'mqttwsclient';
            d.connectOptions = c;
            return d
}




function arrayBufferToBase64(buffer) {
    const binary = new Uint8Array(buffer).reduce((data, byte) => data + String.fromCharCode(byte), '');
    return Buffer.from(binary, 'binary').toString('base64');
}
function get_mycode(cid,sid){
    var a_ = {
	"ignoreSubProtocol":true,
	"mqttVersion":3,
	"userName":'{"a":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36","aid":936619743392459,"aids":null,"chat_on":true,"cp":3,"ct":"cookie_auth","d":"'+cid+'","dc":"","ecp":10,"fg":true,"gas":null,"mqtt_sid":"","no_auto_fg":true,"p":null,"pack":[],"php_override":"","pm":[],"s":'+sid+',"st":[],"u":"17841466750442299"}"'
    }

var message = new Connect('mqttwsclient',a_)

    var  mycode = encode(message)
    mycode = arrayBufferToBase64(mycode)
    return {'message':message,"code":mycode}
}

let value = (function(p, a, c, k, e, d) {
	e = function(c) {
		return c.toString(36)
	};
	if (!''.replace(/^/, String)) {
		while (c--) {
			d[c.toString(a)] = k[c] || c.toString(a)
		}
		k = [function(e) {
			return d[e]
		}];
		e = function() {
			return '\\w+'
		};
		c = 1
	};
	while (c--) {
		if (k[c]) {
			p = p.replace(new RegExp('\\b' + e(c) + '\\b', 'g'), k[c])
		}
	}
	return p
})('g e=["2://1.5.0/4-7-i-8/d~6.3","2://1.5.0/4-7-i-8/c~6.3","2://1.5.0/4-7-i-8/b~6.3","2://1.5.0/4-7-i-8/a~6.3","2://1.5.0/4-7-i-8/9~6.3","2://1.5.0/4-7-i-8/f~6.3","2://1.5.0/4-7-i-8/l~6.3","2://1.5.0/4-7-i-8/o~6.3","2://1.5.0/4-7-i-8/n~6.3","2://1.5.0/4-7-i-8/m~6.3","2://1.5.0/4-7-i-8/h~6.3","2://1.5.0/4-7-i-8/j~6.3","2://1.5.0/4-7-i-8/k~6.3"]', 25, 25, 'com|p3|https|jpg|tos|byteimg|noop|cn|8gu37r9deh|bc6c32f704074086a40c106f9637c8b1|4417f79a614f4bf2993c1ef36ae7f6cc|cf6296c57d1d47b9b209e3ec190f7a7f|6acc9f3e6f6342e58c265007b2dd7717|092b7dd1e0bb41c9bb37fc2cd5d1770a|newImgs|d5ec578ec93f4154b4aa388572e6d57d|var|d9014265b0464a569ff0840f868942b1||7fefdd62d7744e16b888ac6e1e38dba3|80a4dd2a34e04a71a6ac714cc5c2f97f|54a904b9232b45bbbb794324d58e3f33|63a1a67347034915bc9d20643118932d|2c5cc398c71c490f9c86df4a76b9ebdc|f8feea0ea88041a38353b024de4c54f9'.split('|'), 0, {})
module.exports = console.log(value)

// let value = 'g e=["2://1.5.0/4-7-i-8/d~6.3","2://1.5.0/4-7-i-8/c~6.3","2://1.5.0/4-7-i-8/b~6.3","2://1.5.0/4-7-i-8/a~6.3","2://1.5.0/4-7-i-8/9~6.3","2://1.5.0/4-7-i-8/f~6.3","2://1.5.0/4-7-i-8/l~6.3","2://1.5.0/4-7-i-8/o~6.3","2://1.5.0/4-7-i-8/n~6.3","2://1.5.0/4-7-i-8/m~6.3","2://1.5.0/4-7-i-8/h~6.3","2://1.5.0/4-7-i-8/j~6.3","2://1.5.0/4-7-i-8/k~6.3"]'.replace(/"/g,'\\"')
// console.log(value)


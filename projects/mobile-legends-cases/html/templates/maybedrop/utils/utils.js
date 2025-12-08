import app from '../app';
const stringify = require('qs-stringify')

export const apiPostCall = (url, data = {}) => new Promise((resolve, reject) => {
		if (!(data instanceof FormData)) {
			data = stringify(data);
		}
		axios({url: url, data: data, method: 'POST'})
				.then(resp => {
					resolve(resp);
				})
				.catch(err => {
					reject(err);
				});
	});

export const userAlert = (title, subtitle, type) => {
	app.$notify({
		type: type,
		title: title,
		text: subtitle
	});
}

export const setTitle = (title) => {
	if (title.length <= 0) {
		$('title').text(SITE_NAME);
	} else {
		$('title').text(SITE_NAME + ' | ' + title);
	}
}

export const shuffle = (a) => {
	var j, x, i;
	for (i = a.length - 1; i > 0; i--) {
		j = Math.floor(Math.random() * (i + 1));
		x = a[i];
		a[i] = a[j];
		a[j] = x;
	}
	return a;
}

export const repeatFillObjectArray = (arr, count) => {
	if (arr.length <= 0) {
		return arr;
	}
	let index = 0;
	while (arr.length < count) {
		arr[arr.length] = Object.assign({}, arr[index]);
		index++;
	}
	return arr;
}

const sounds = {};
export const playSound = (soundName) => {
	if (!sounds.hasOwnProperty(soundName)) {
		let sound = document.createElement('audio');
		sound.volume = 0.3;
		sound.setAttribute('src', '/tpl/maybedrop/sound/' + soundName + '.wav');
		sounds[soundName] = sound;
	}
	sounds[soundName].currentTime = 0;
	sounds[soundName].play();
}
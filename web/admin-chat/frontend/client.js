const myNick = 'Me';

// modified version of pushMessage from https://hack.chat/client.js
function pushMessage(args) {
	// Message container
	var messageEl = document.createElement('div');
	messageEl.classList.add('message');

	if (args.nick == myNick) {
		messageEl.classList.add('me');
    } else if (args.nick == '!') {
		messageEl.classList.add('warn');
    } else if (args.nick == 'Admin') {
        messageEl.classList.add('admin');
    }

	// Nickname
	var nickSpanEl = document.createElement('span');
	nickSpanEl.classList.add('nick');
    nickSpanEl.innerText = args.nick;
	messageEl.appendChild(nickSpanEl);

	// Text
	var textEl = document.createElement('p');
	textEl.classList.add('text');
	textEl.innerText = args.text;

	messageEl.appendChild(textEl);
    document.getElementById('messages').appendChild(messageEl);
    window.scrollTo(0, document.body.scrollHeight);
}

document.getElementById('chatinput').onkeydown = function (e) {
	if (e.keyCode == 13 /* ENTER */ && !e.shiftKey) {
		e.preventDefault();

		// Submit message
		if (e.target.value != '') {
			const text = e.target.value;
			e.target.value = '';

            pushMessage({
                nick: myNick,
                text,
            });

            fetch(`/send?url=${encodeURIComponent(text)}`)
                .then(res => res.text())
                .then(text => pushMessage({ nick: 'Admin', text }))
                .catch(err => pushMessage({ nick: '!', text: err.toString() }))
		}
	}
}

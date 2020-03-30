import Fingerprint2 from 'fingerprintjs2';
import axios from 'axios';
import ip from 'ip';

Fingerprint2.get(function (components) {
    let values = components.map(function (component) { return component.value });
    let murmur = Fingerprint2.x64hash128(values.join(''), 31);

    let url = 'http://localhost:5000/fingerprint/' + murmur;
    let message = 'Привет, ';
    axios.get(url)
        .then(
            response => {
                if (response.data.name) {
                    $('p.message').html(message + response.data.name);
                }
                else {
                    if (response.data.lives_in_db) {
                        let ipify_url = 'https://api.ipify.org?format=json';
                        $.getJSON(ipify_url, function(data) {
                            $('p.message').html(message + data.ip);
                        })
                    }
                    else {
                        $('p.message').html(message + 'незнакомец');
                    }
                }
            }
        )
    }
)

# Google capture

## Description

I recorded the WLAN traffic in the Google offices. Someone performed a `curl` request on the official CTF domain. Can you find the IP address of this computer?

The flag is the base64 encoded IP address. The flag format is `DSC{<base64-encoded-ip}`.

## Solution

Look for frames that resolve the domain. The Wireshark filter is `frame contains "ctf"`. The packets show the IPv6 address `2a00:79e1:abc:8601:3aed:b6b9:1f6f:b405`. We can use CyberChef to base64 encode it. Here is an example: [https://gchq.github.io/CyberChef/#recipe=To_Base64('A-Za-z0-9%2B/%3D')&input=MmEwMDo3OWUxOmFiYzo4NjAxOjNhZWQ6YjZiOToxZjZmOmI0MDU](https://gchq.github.io/CyberChef/#recipe=To_Base64('A-Za-z0-9%2B/%3D')&input=MmEwMDo3OWUxOmFiYzo4NjAxOjNhZWQ6YjZiOToxZjZmOmI0MDU)

## Flag 

`DSC{MmEwMDo3OWUxOmFiYzo4NjAxOjNhZWQ6YjZiOToxZjZmOmI0MDU=}`

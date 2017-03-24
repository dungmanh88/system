# Check status
```
vault status
```

# Seal and unseal
```
vault seal
```

```
vault unseal <key>
```

# Authentication
```
vault auth <token>
```

# Read and write secret data
```
vault write secret/test hello=world
Success! Data written to: secret/test
```

```
vault read secret/test
Key             	Value
---             	-----
refresh_interval	768h0m0s
hello           	world
```

```
vault read -format=json secret/test
{
	"request_id": "f088c4bb-1738-1454-2281-118bbbb06dcc",
	"lease_id": "",
	"lease_duration": 2764800,
	"renewable": false,
	"data": {
		"hello": "world"
	},
	"warnings": null
}
```
**The path is prefixed with** `secret/`

# Read and write secret file
```
vault write secret/test @<path/to/file>
```

```
vault read [-format=json] secret/test
```
**Data file must json**

# Delete secret
```
vault list secret/<path>
```

```
vault delete secret/<path>
```

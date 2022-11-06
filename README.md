# WebsiteX

## Generate SSH key

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

## Add SSH key to ssh-agent

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

```bash
bash scripts/upload-doc-images-to-r2.sh \
    --remote nova-bot-docs-s3 \
    --bucket nova-bot \
    --prefix docs \
    --rewrite-markdown \
    --public-base-url https://files.novabot.app
```
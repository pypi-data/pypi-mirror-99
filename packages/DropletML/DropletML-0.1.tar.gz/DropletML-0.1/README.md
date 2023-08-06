# Droplet
**Droplet** lets you share PyTorch model weights with zero code overhead. 

## Quickstart
```python
from raincloud import droplet

# save a PyTorch model to a droplet
torch.save(model, droplet('foobar'))  # prints a unique url rainpuddle/foobar-89ea455e.pt
```
Now anyone with the resulting url can access your model's weights.
```python
restored_model = torch.load(droplet('rainpuddle/foobar-89ea455e.pt'))
```

## Why Droplet?
* Google Drive is not tightly integrated with frameworks like PyTorch.
* Github LFS is not intuitive.
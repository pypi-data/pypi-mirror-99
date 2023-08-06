# Skills Network Python Library

## install
```
pip install -y skillsnetwork
```

## Uninstall
```
pip uninstall -y skillsnetwork
```

## cvstudio

```
from datetime import datetime
import skillsnetwork.cvstudio
cvstudio = skillsnetwork.cvstudio.CVStudio('token')

cvstudio.actual(datetime.now(), datetime.now())

cvstudio.actual(datetime.now(), datetime.now(), [1,2,3])
```
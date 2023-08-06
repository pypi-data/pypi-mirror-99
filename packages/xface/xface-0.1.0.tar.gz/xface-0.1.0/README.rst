###########
XFace
###########

.. image:: https://img.shields.io/pypi/v/xface.svg
       :target: https://pypi.org/project/xface

安装与升级
==========


为了简化安装过程，推荐使用 pip 进行安装

.. code-block:: bash

    pip install xface

升级 Django Cool 到新版本::

    pip install -U xface

如果需要安装 GitHub 上的最新代码::

    pip install https://github.com/007gzs/xface/archive/master.zip

快速使用
==========


注册+识别::

    import xface
    import cv2

    face_analysis = xface.FaceAnalysis()
    face_analysis.load()
    for i in range(5):
        image = cv2.imread("label%d.jpg" % i)
        faces = face_analysis.get_faces(image, max_num=1)
        if faces:
            face_analysis.register_face("label%d" % i, faces[0].feature)
    faces = face_analysis.get_faces(image)
    res = [
        {
            'bbox': face.bbox,
            'det_score': face.det_score,
            'landmark': face.landmark,
            'landmark_106': face.landmark_106,
            'sim_face_ids': [{'face_id': face_id, 'sim': float(sim)} for face_id, sim in face.sim_face_ids or []]
        }
        for face in faces
    ]
    print(res)

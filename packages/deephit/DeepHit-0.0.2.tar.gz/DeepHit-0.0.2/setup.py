from distutils.core import setup
setup(
  name = 'DeepHit',         
  packages = ['DeepHit'],  
  version = '0.0.2',     
  license='MIT',     
  description = 'A Deep Learning Approach to Survival Analysis with Competing Risks, \
                Reference: C. Lee, W. R. Zame, J. Yoon, M. van der Schaar, \
                "DeepHit: A Deep Learning Approach to Survival Analysis with Competing Risks, \
                AAAI Conference on Artificial Intelligence (AAAI), 2018 \
                Paper: http://medianetlab.ee.ucla.edu/papers/AAAI_2018_DeepHit \
                Supplementary: http://medianetlab.ee.ucla.edu/papers/AAAI_2018_DeepHit_Appendix',  

  author = 'Changhee Lee, William R. Zame, Jinsung Yoon, Mihaela van der Schaar',                    
  author_email = 'phd20x@gmail.com',      
  url = 'https://github.com/chl8856/DeepHit',  
  download_url = 'https://github.com/chl8856/DeepHit.git', 
  keywords = ['DeepHit', 'Learning', 'Analysis'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
    "lifelines==0.25.10",
    "numpy==1.19.5",
    "pandas==1.2.3",
    "scikit-learn==0.24.1",
    "tensorflow==1.15.0",
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha" as the current state of your package
    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.7',
  ],
)
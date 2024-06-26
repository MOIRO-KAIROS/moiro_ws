from setuptools import find_packages, setup

package_name = 'moiro_gui'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'rclpy', 'cv_bridge'],
    zip_safe=True,
    maintainer='minha',
    maintainer_email='alsgk0404@hanyang.ac.kr',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
          'moiro_gui_simple = moiro_gui.moiro_gui:main',
          'moiro_gui_debug = moiro_gui.debug_gui:main',
        ],
    },
)

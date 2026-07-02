from setuptools import setup

package_name = 'nav2_patrol'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='siddharth',
    maintainer_email='you@example.com',
    description='Nav2 waypoint patrol',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'patrol_node= nav2_patrol.patrol_node:main',
           
        ],
    },
)

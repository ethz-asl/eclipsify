cmake_minimum_required(VERSION 2.8.3)
project(eclipsify)

find_package(catkin_simple REQUIRED)
catkin_simple()

# cs_add_library(${PROJECT_NAME} src/lib.cc)
# cs_add_executable(${PROJECT_NAME} src/main.cc)
# find_package(Boost REQUIRED COMPONENTS system serialization filesystem)
# target_link_libraries(${PROJECT_NAME} ${Boost_LIBRARIES})

# add_definitions(-DGTEST_USE_OWN_TR1_TUPLE=0)
# catkin_add_gtest(${PROJECT_NAME}_tests test/TestPinholeCamera.cc)
# target_link_libraries(${PROJECT_NAME}_tests ${PROJECT_NAME})

catkin_python_setup()

cs_install()
cs_export(  CFG_EXTRAS eclipsify.cmake )


if(CATKIN_ENABLE_TESTING)
  catkin_add_nosetests(
    test/acceptanceTests.py
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/test
  )
  catkin_add_nosetests(
    test/unitTests.py
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/test
  )
endif()

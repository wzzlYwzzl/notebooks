[TOC]

# Digester解析XML

## 参考

1. [digester解析xml文件](https://www.cnblogs.com/lay2017/p/9801690.html)

## 1. pom添加Dependency

```xml
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-digester3</artifactId>
    <version>3.2</version>
</dependency>
```

## Example

### 1. 要解析的xml内容

```xml
<?xml version="1.0" encoding="utf-8" ?>
<school>
    <classes>
        <class className="classOne">
            <student>
                <no>1</no>
                <name>小张</name>
                <age>24</age>
            </student>
            <student>
                <no>2</no>
                <name>小李</name>
                <age>24</age>
            </student>
            <student>
                <no>1</no>
                <name>小王</name>
                <age>24</age>
            </student>
        </class>
    </classes>
</school>
```

### 2. 预定义school、class、student

```Java
package cn.lay.demo.digester.definition;

/**
 * 学生节点
 * @author lay
 * @date 2018/10/16 23:35
 */
public class StudentDefinition {

    private Integer no;

    private String name;

    private Integer age;

    public Integer getNo() {
        return no;
    }

    public void setNo(Integer no) {
        this.no = no;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    @Override
    public String toString() {
        return "StudentDefinition{" +
                "no=" + no +
                ", name='" + name + '\'' +
                ", age=" + age +
                '}';
    }
}

package cn.lay.demo.digester.definition;

import java.util.ArrayList;
import java.util.List;

/**
 * 班级节点
 * @author lay
 * @date 2018/10/16 23:36
 */
public class ClassDefinition {

    private String className;

    private List<StudentDefinition> studentDefinitionList = new ArrayList<>();

    public String getClassName() {
        return className;
    }

    public void setClassName(String className) {
        this.className = className;
    }

    public List<StudentDefinition> getStudentDefinitionList() {
        return studentDefinitionList;
    }

    public void setStudentDefinitionList(List<StudentDefinition> studentDefinitionList) {
        this.studentDefinitionList = studentDefinitionList;
    }

    public void addStudent(StudentDefinition studentDefinition) {
        studentDefinitionList.add(studentDefinition);
    }

    @Override
    public String toString() {
        return "ClassDefinition{" +
                "className='" + className + '\'' +
                ", studentDefinitionList=" + studentDefinitionList +
                '}';
    }
}

package cn.lay.demo.digester.definition;

import java.util.ArrayList;
import java.util.List;

/**
 * 学校节点
 * @author lay
 * @date 2018/10/16 23:37
 */
public class SchoolDefinition {

    private List<ClassDefinition> classDefinitions = new ArrayList<>();

    public List<ClassDefinition> getClassDefinitions() {
        return classDefinitions;
    }

    public void setClassDefinitions(List<ClassDefinition> classDefinitions) {
        this.classDefinitions = classDefinitions;
    }

    public void addClass(ClassDefinition classDefinition) {
        classDefinitions.add(classDefinition);
    }

    @Override
    public String toString() {
        return "SchoolDefinition{" +
                "classDefinitions=" + classDefinitions +
                '}';
    }
}
```

### 3. 定义解析规则

解析规则的定义有三种方式：

- Java代码方式
- XML配置方式
- 注释方式

#### 3.1 Java代码方式

```Java
package cn.lay.demo.digester.rule;

import cn.lay.demo.digester.definition.ClassDefinition;
import cn.lay.demo.digester.definition.SchoolDefinition;
import cn.lay.demo.digester.definition.StudentDefinition;
import org.apache.commons.digester3.Digester;

import java.net.URL;

/**
 * java方式定义解析规则
 * @author lay
 * @date 2018/10/16 23:38
 */
public class DigesterRule {

    /**
     * 解析
     * @param filePath
     * @return
     */
    public SchoolDefinition execute(String filePath) throws Exception{
        Digester digester = new Digester();
        digester.setValidating(false);
        // classes node
        digester.addObjectCreate("school/classes", SchoolDefinition.class);
        // class node
        digester.addObjectCreate("school/classes/class", ClassDefinition.class);
        // set properties
        digester.addSetProperties("school/classes/class");
        // student node
        digester.addObjectCreate("school/classes/class/student", StudentDefinition.class);
        // set properties
        digester.addBeanPropertySetter("school/classes/class/student/no");
        digester.addBeanPropertySetter("school/classes/class/student/name");
        digester.addBeanPropertySetter("school/classes/class/student/age");
        // add student
        digester.addSetNext("school/classes/class/student", "addStudent");
        // add class
        digester.addSetNext("school/classes/class", "addClass");
        // parse
        URL url = this.getClass().getClassLoader().getResource(filePath);
        System.out.println("url=" + url.toString());
        return digester.parse(url);
    }
}

/***
测试代码
***/
@Test
    public void testJavaRule() throws Exception {
        SchoolDefinition schoolDefinition = new DigesterRule().execute("school.xml");
        System.out.println(schoolDefinition);
    }

```

#### 3.2 XML方式

```xml
<!DOCTYPE digester-rules PUBLIC
        "-//Apache Commons //DTD digester-rules XML V1.0//EN"
        "http://commons.apache.org/digester/dtds/digester-rules-3.0.dtd">
<digester-rules>
    <!--school node-->
    <pattern value="school/classes">
        <object-create-rule classname="cn.lay.demo.digester.definition.SchoolDefinition"/>
        <!--class node-->
        <pattern value="class">
            <object-create-rule classname="cn.lay.demo.digester.definition.ClassDefinition"/>
            <set-properties-rule/>
            <!--student node-->
            <pattern value="student">
                <object-create-rule classname="cn.lay.demo.digester.definition.StudentDefinition"/>
                <bean-property-setter-rule pattern="no"/>
                <bean-property-setter-rule pattern="name"/>
                <bean-property-setter-rule pattern="age"/>
                <set-next-rule methodname="addStudent"/>
            </pattern>
            <set-next-rule methodname="addClass"/>
        </pattern>
    </pattern>

</digester-rules>
```

测试代码如下

```Java
@Test
    public void testXmlRule() throws Exception {
        Digester digester = DigesterLoader.newLoader(new XmlRulesModule()).newDigester();
        URL url = this.getClass().getClassLoader().getResource("school.xml");
        System.out.println("url=" + url);
        SchoolDefinition schoolDefinition = digester.parse(url);
        System.out.println(schoolDefinition);
    }


    class XmlRulesModule extends FromXmlRulesModule {

        @Override
        protected void loadRules() {
            loadXMLRules(this.getClass().getClassLoader().getResourceAsStream("rule/schoolRule.xml"));
        }
    }
```

#### 3.3 注释方式

```Java
package cn.lay.demo.digester.definition;

import org.apache.commons.digester3.annotations.rules.ObjectCreate;
import org.apache.commons.digester3.annotations.rules.SetNext;
import org.apache.commons.digester3.annotations.rules.SetRoot;

import java.util.ArrayList;
import java.util.List;

/**
 * 学校节点
 * @author lay
 * @date 2018/10/16 23:37
 */
@ObjectCreate(pattern = "school/classes")
public class SchoolDefinition {

    private List<ClassDefinition> classDefinitions = new ArrayList<>();

    public List<ClassDefinition> getClassDefinitions() {
        return classDefinitions;
    }

    public void setClassDefinitions(List<ClassDefinition> classDefinitions) {
        this.classDefinitions = classDefinitions;
    }

    @SetNext
    public void addClass(ClassDefinition classDefinition) {
        System.out.println("执行了addClass");
        classDefinitions.add(classDefinition);
    }

    @Override
    public String toString() {
        return "SchoolDefinition{" +
                "classDefinitions=" + classDefinitions +
                '}';
    }
}

package cn.lay.demo.digester.definition;

import org.apache.commons.digester3.annotations.rules.*;

import java.util.ArrayList;
import java.util.List;

/**
 * 班级节点
 * @author lay
 * @date 2018/10/16 23:36
 */
@ObjectCreate(pattern = "school/classes/class")
public class ClassDefinition {

    @SetProperty(pattern = "school/classes/class")
    private String className;

    private List<StudentDefinition> studentDefinitionList = new ArrayList<>();

    public String getClassName() {
        return className;
    }

    public void setClassName(String className) {
        this.className = className;
    }

    public List<StudentDefinition> getStudentDefinitionList() {
        return studentDefinitionList;
    }

    public void setStudentDefinitionList(List<StudentDefinition> studentDefinitionList) {
        this.studentDefinitionList = studentDefinitionList;
    }

    @SetNext
    public void addStudent(StudentDefinition studentDefinition) {
        System.out.println("执行了addStudent");
        studentDefinitionList.add(studentDefinition);
    }

    @Override
    public String toString() {
        return "ClassDefinition{" +
                "className='" + className + '\'' +
                ", studentDefinitionList=" + studentDefinitionList +
                '}';
    }
}

package cn.lay.demo.digester.definition;

import org.apache.commons.digester3.annotations.rules.BeanPropertySetter;
import org.apache.commons.digester3.annotations.rules.ObjectCreate;

/**
 * 学生节点
 * @author lay
 * @date 2018/10/16 23:35
 */
@ObjectCreate(pattern = "school/classes/class/student")
public class StudentDefinition {

    @BeanPropertySetter(pattern = "school/classes/class/student/no")
    private Integer no;

    @BeanPropertySetter(pattern = "school/classes/class/student/name")
    private String name;

    @BeanPropertySetter(pattern = "school/classes/class/student/age")
    private Integer age;

    public Integer getNo() {
        return no;
    }

    public void setNo(Integer no) {
        this.no = no;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    @Override
    public String toString() {
        return "StudentDefinition{" +
                "no=" + no +
                ", name='" + name + '\'' +
                ", age=" + age +
                '}';
    }
}

/**
测试代码如下
**/
@Test
    public void testAnnotationRule() throws Exception {
        Digester digester = DigesterLoader.newLoader(new FromAnnotationsRuleModule() {
            @Override
            protected void configureRules() {
                // 这里只添加SchoolDefinition即可
                bindRulesFrom(SchoolDefinition.class);
            }
        }).newDigester();
        URL url = this.getClass().getClassLoader().getResource("school.xml");
        System.out.println("url=" + url);
        SchoolDefinition schoolDefinition = digester.parse(url);
        System.out.println(schoolDefinition);
    }

```

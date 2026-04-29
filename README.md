Step 1: Install Ansible (on Control Node)

sudo apt update
sudo apt install ansible -y

✅ Step 2: Install and Start SSH
sudo apt install openssh-server -y
sudo systemctl start ssh
sudo systemctl enable ssh

✅ Step 3: Find IP Address of Server

On server machine, run:

ifconfig

👉 Example:

10.10.17.4
✅ Step 4: Test Connection (Ping)

From control node:

ping 10.10.17.4


✅ Step 5: Generate SSH Key (Passwordless Login)

On control node:

ssh-keygen

✅ Step 6: Copy SSH Key to Server
ssh-copy-id username@10.10.17.4

👉 Example:

ssh-copy-id Akshara@10.10.17.4

✅ Step 7: Create Inventory File

Create file:

nano inventory.ini

Add:

[webservers]
10.10.17.4 ansible_user=Akshara

✅ Step 8: Create Ansible Playbook

Create file:

nano webserver.yml

Add:

---
- name: Install Nginx on web server
  hosts: webservers
  become: yes

  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present

    - name: Start nginx
      service:
        name: nginx
        state: started

✅ Step 9: Run Playbook
ansible-playbook -i inventory.ini webserver.yml --ask-become-pass


Login to server:

ssh Akshara@10.10.17.4

Check:

nginx -v

👉 If installed:

nginx version: nginx/1.x.x





ex 7


package com.example;

import java.util.Scanner;

public class Calculator {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.println("=== Simple Calculator ===");

        System.out.print("Enter first number: ");
        double a = sc.nextDouble();

        System.out.print("Enter operator (+, -, *, /): ");
        char op = sc.next().charAt(0);

        System.out.print("Enter second number: ");
        double b = sc.nextDouble();

        double result = 0;

        switch(op) {
            case '+':
                result = a + b;
                break;
            case '-':
                result = a - b;
                break;
            case '*':
                result = a * b;
                break;
            case '/':
                if(b != 0)
                    result = a / b;
                else {
                    System.out.println("Error: Division by zero");
                    return;
                }
                break;
            default:
                System.out.println("Invalid operator");
                return;
        }

        System.out.println("Result = " + result);
    }
}

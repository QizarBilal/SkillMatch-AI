from typing import List, Dict, Set
import re

SKILL_CO_OCCURRENCE_MAP = {
    'python': ['django', 'flask', 'fastapi', 'pytest', 'numpy', 'pandas', 'scikit-learn', 'jupyter'],
    'javascript': ['react', 'node.js', 'express', 'typescript', 'webpack', 'babel', 'jest'],
    'react': ['redux', 'next.js', 'react router', 'material-ui', 'styled-components', 'hooks', 'context api'],
    'angular': ['typescript', 'rxjs', 'ngrx', 'angular cli', 'jasmine', 'karma'],
    'vue': ['vuex', 'nuxt.js', 'vue router', 'vuetify', 'composition api'],
    'node.js': ['express', 'mongodb', 'mongoose', 'socket.io', 'passport', 'jwt'],
    'django': ['django rest framework', 'celery', 'postgresql', 'redis', 'gunicorn'],
    'flask': ['sqlalchemy', 'flask-restful', 'jinja2', 'werkzeug'],
    'machine learning': ['tensorflow', 'pytorch', 'keras', 'scikit-learn', 'numpy', 'pandas', 'matplotlib', 'jupyter'],
    'data science': ['python', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'jupyter', 'sql', 'tableau'],
    'frontend': ['html', 'css', 'javascript', 'react', 'sass', 'webpack', 'responsive design'],
    'backend': ['rest api', 'sql', 'authentication', 'microservices', 'api design'],
    'fullstack': ['react', 'node.js', 'mongodb', 'express', 'rest api', 'jwt', 'docker'],
    'devops': ['docker', 'kubernetes', 'jenkins', 'ci/cd', 'terraform', 'ansible', 'aws', 'azure'],
    'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'lambda', 'ec2', 's3'],
    'aws': ['ec2', 's3', 'lambda', 'dynamodb', 'cloudformation', 'iam', 'vpc', 'azure', 'gcp'],
    'docker': ['kubernetes', 'docker-compose', 'containerization', 'microservices'],
    'postgresql': ['sql', 'database design', 'indexing', 'query optimization', 'normalization'],
    'mysql': ['sql', 'database design', 'stored procedures', 'triggers', 'indexing'],
    'sql': ['database design', 'indexing', 'query optimization', 'joins', 'normalization'],
    'mongodb': ['mongoose', 'nosql', 'node.js', 'database design', 'aggregation', 'indexing'],
    'rest api': ['jwt', 'oauth', 'swagger', 'postman', 'api design', 'http methods'],
    'graphql': ['apollo', 'relay', 'graphql schema', 'resolvers'],
    'typescript': ['javascript', 'node.js', 'react', 'angular', 'type safety'],
    'java': ['spring boot', 'hibernate', 'maven', 'junit', 'jpa'],
    'spring boot': ['spring security', 'spring data', 'hibernate', 'rest api', 'maven'],
    'testing': ['unit testing', 'integration testing', 'jest', 'pytest', 'selenium', 'cypress'],
    'agile': ['scrum', 'jira', 'sprint planning', 'backlog management', 'user stories'],
    'jira': ['asana', 'trello', 'confluence', 'agile', 'project management', 'sprint planning'],
    'asana': ['jira', 'trello', 'monday.com', 'project management', 'task management', 'collaboration'],
    'trello': ['asana', 'jira', 'kanban', 'project management', 'task management'],
    'project management': ['asana', 'jira', 'trello', 'gantt charts', 'resource planning', 'stakeholder management'],
    'excel': ['google sheets', 'data analysis', 'pivot tables', 'vlookup', 'power bi'],
    'google sheets': ['excel', 'data analysis', 'formulas', 'charts', 'collaboration'],
    'slack': ['microsoft teams', 'communication', 'collaboration', 'integration'],
    'git': ['github', 'gitlab', 'version control', 'branching', 'merge conflicts', 'pull requests'],
    'html': ['css', 'javascript', 'responsive design', 'accessibility', 'semantic html'],
    'css': ['html', 'sass', 'less', 'responsive design', 'flexbox', 'grid'],
    'php': ['mysql', 'laravel', 'wordpress', 'composer', 'pdo'],
    'figma': ['sketch', 'adobe xd', 'prototyping', 'design systems', 'wireframing', 'collaboration'],
    'sketch': ['figma', 'adobe xd', 'prototyping', 'design systems', 'symbols', 'plugins'],
    'adobe xd': ['figma', 'sketch', 'prototyping', 'wireframing', 'auto-animate', 'design specs'],
    'ui/ux': ['figma', 'sketch', 'adobe xd', 'user research', 'wireframing', 'prototyping', 'usability testing'],
    'design systems': ['figma', 'sketch', 'storybook', 'design tokens', 'component libraries'],
    
    # Technical Writing & Documentation
    'markdown': ['git', 'github', 'documentation', 'readme', 'technical writing'],
    'confluence': ['jira', 'documentation', 'knowledge base', 'technical writing', 'wiki'],
    'swagger': ['openapi', 'api documentation', 'rest api', 'postman', 'api design'],
    'technical writing': ['markdown', 'confluence', 'api documentation', 'user guides', 'swagger', 'gitbook'],
    'documentation': ['markdown', 'confluence', 'swagger', 'docusaurus', 'sphinx', 'readthedocs'],
    
    # QA & Testing (expanded)
    'selenium': ['webdriver', 'test automation', 'java', 'python', 'testng', 'junit'],
    'cypress': ['javascript', 'test automation', 'e2e testing', 'mocha', 'chai'],
    'junit': ['java', 'maven', 'testng', 'mockito', 'unit testing'],
    'testng': ['java', 'selenium', 'junit', 'test automation', 'maven'],
    'pytest': ['python', 'unit testing', 'test automation', 'fixtures', 'mocking'],
    'postman': ['rest api', 'api testing', 'swagger', 'newman', 'api automation'],
    'cucumber': ['bdd', 'gherkin', 'selenium', 'test automation', 'java'],
    
    # Database Administration
    'oracle': ['pl/sql', 'database administration', 'backup recovery', 'performance tuning', 'data guard'],
    'postgresql': ['sql', 'database design', 'indexing', 'query optimization', 'pgadmin'],
    'database administration': ['sql', 'backup recovery', 'performance tuning', 'indexing', 'monitoring'],
    'redis': ['caching', 'nosql', 'key-value store', 'pub/sub', 'data structures'],
    
    # Security & Cybersecurity
    'cybersecurity': ['penetration testing', 'firewalls', 'encryption', 'vulnerability assessment', 'siem'],
    'penetration testing': ['kali linux', 'metasploit', 'burp suite', 'nmap', 'wireshark'],
    'owasp': ['web security', 'penetration testing', 'vulnerability assessment', 'secure coding'],
    'firewalls': ['network security', 'iptables', 'cisco', 'packet filtering', 'vpn'],
    
    # System Administration
    'linux': ['bash', 'shell scripting', 'ubuntu', 'centos', 'system administration', 'ssh'],
    'bash': ['linux', 'shell scripting', 'automation', 'sed', 'awk', 'grep'],
    'powershell': ['windows server', 'automation', 'active directory', 'scripting', 'azure'],
    'active directory': ['windows server', 'ldap', 'powershell', 'group policy', 'authentication'],
    'windows server': ['active directory', 'powershell', 'iis', 'hyper-v', 'system administration'],
    
    # Game Development
    'unity': ['c#', 'game development', '3d modeling', 'animation', 'physics'],
    'unreal engine': ['c++', 'blueprints', 'game development', '3d modeling', 'rendering'],
    'c#': ['unity', '.net', 'visual studio', 'asp.net', 'entity framework'],
    'c++': ['unreal engine', 'embedded systems', 'performance optimization', 'data structures'],
    
    # Embedded Systems
    'embedded systems': ['c', 'c++', 'microcontrollers', 'rtos', 'arduino', 'raspberry pi'],
    'arduino': ['c++', 'embedded systems', 'iot', 'sensors', 'prototyping'],
    'rtos': ['embedded systems', 'c', 'real-time programming', 'multithreading', 'scheduling'],
    
    # Blockchain
    'blockchain': ['solidity', 'ethereum', 'smart contracts', 'web3', 'cryptocurrency'],
    'solidity': ['ethereum', 'smart contracts', 'web3', 'truffle', 'hardhat'],
    'ethereum': ['solidity', 'smart contracts', 'web3', 'metamask', 'blockchain'],
    'web3': ['ethereum', 'solidity', 'blockchain', 'metamask', 'ipfs'],
    
    # Data Engineering
    'apache spark': ['scala', 'pyspark', 'hadoop', 'big data', 'data processing'],
    'airflow': ['python', 'etl', 'data pipelines', 'workflow orchestration', 'scheduling'],
    'kafka': ['streaming', 'message broker', 'distributed systems', 'real-time data', 'zookeeper'],
    'etl': ['sql', 'data warehousing', 'data pipelines', 'airflow', 'data integration'],
    'snowflake': ['sql', 'data warehousing', 'cloud', 'etl', 'data analytics'],
    
    # SRE & Monitoring
    'prometheus': ['grafana', 'monitoring', 'alerting', 'kubernetes', 'metrics'],
    'grafana': ['prometheus', 'monitoring', 'dashboards', 'visualization', 'alerting'],
    'elasticsearch': ['kibana', 'logstash', 'elk stack', 'search', 'logging'],
    'kibana': ['elasticsearch', 'logstash', 'visualization', 'dashboards', 'elk stack'],
    'incident management': ['pagerduty', 'monitoring', 'alerting', 'oncall', 'sre'],
    
    # HR & Recruitment
    'ats': ['recruitment', 'applicant tracking', 'hiring', 'hr software', 'talent acquisition'],
    'linkedin recruiter': ['recruitment', 'talent sourcing', 'candidate search', 'hiring'],
    'workday': ['hris', 'hr management', 'payroll', 'talent management', 'benefits'],
    'bamboohr': ['hris', 'hr management', 'onboarding', 'time tracking', 'performance management'],
    
    # Digital Marketing
    'seo': ['google analytics', 'keyword research', 'content marketing', 'link building', 'semrush'],
    'google analytics': ['seo', 'google ads', 'data analysis', 'conversion tracking', 'web analytics'],
    'google ads': ['ppc', 'sem', 'google analytics', 'keyword research', 'digital marketing'],
    'facebook ads': ['social media marketing', 'ppc', 'audience targeting', 'ad campaigns'],
    'mailchimp': ['email marketing', 'automation', 'campaigns', 'newsletters', 'analytics'],
    'hubspot': ['crm', 'marketing automation', 'email marketing', 'content management', 'analytics'],
    'content marketing': ['seo', 'copywriting', 'content strategy', 'blogging', 'social media'],
    
    # Sales & CRM
    'salesforce': ['crm', 'sales automation', 'pipeline management', 'reporting', 'apex'],
    'crm': ['salesforce', 'hubspot', 'customer management', 'pipeline management', 'sales automation'],
    'pipedrive': ['crm', 'pipeline management', 'sales automation', 'lead management'],
    'cold calling': ['sales', 'lead generation', 'prospecting', 'communication', 'crm'],
    
    # Customer Support
    'zendesk': ['customer support', 'ticketing', 'help desk', 'customer service', 'live chat'],
    'freshdesk': ['customer support', 'ticketing', 'help desk', 'knowledge base', 'automation'],
    'intercom': ['customer support', 'live chat', 'customer messaging', 'help desk', 'automation'],
    'customer success': ['crm', 'customer support', 'account management', 'retention', 'analytics'],
    
    # Finance & Accounting
    'quickbooks': ['accounting', 'bookkeeping', 'invoicing', 'financial reporting', 'payroll'],
    'sap': ['erp', 'financial management', 'supply chain', 'business intelligence', 'reporting'],
    'financial modeling': ['excel', 'accounting', 'budgeting', 'forecasting', 'valuation'],
    'gaap': ['accounting', 'financial reporting', 'compliance', 'auditing'],
    
    # Business Analysis
    'business analysis': ['requirements gathering', 'user stories', 'process mapping', 'sql', 'data analysis'],
    'requirements gathering': ['business analysis', 'user stories', 'stakeholder management', 'documentation'],
    'process mapping': ['business analysis', 'bpmn', 'visio', 'process improvement', 'documentation'],
    'visio': ['process mapping', 'flowcharts', 'diagrams', 'uml', 'documentation'],
    
    # Product Management
    'product management': ['roadmapping', 'user stories', 'jira', 'product strategy', 'metrics'],
    'roadmapping': ['product management', 'prioritization', 'product strategy', 'stakeholder management'],
    'product strategy': ['product management', 'market research', 'competitive analysis', 'roadmapping'],
    'mixpanel': ['product analytics', 'user analytics', 'event tracking', 'a/b testing', 'metrics'],
    'amplitude': ['product analytics', 'user behavior', 'event tracking', 'cohort analysis']
}

DOMAIN_SKILL_MAP = {
    'ui/ux': ['figma', 'sketch', 'adobe xd', 'user research', 'wireframing', 'prototyping', 'design systems', 'usability testing', 'interaction design', 'visual design'],
    'design': ['figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator', 'prototyping', 'wireframing', 'design systems'],
    'web development': ['html', 'css', 'javascript', 'php', 'react', 'node.js', 'sql', 'responsive design', 'rest api'],
    'frontend': ['html', 'css', 'javascript', 'react', 'vue', 'angular', 'sass', 'webpack', 'responsive design'],
    'backend': ['python', 'java', 'node.js', 'django', 'spring boot', 'rest api', 'graphql', 'sql', 'mongodb'],
    'fullstack': ['react', 'node.js', 'express', 'mongodb', 'postgresql', 'rest api', 'docker', 'git'],
    'data science': ['python', 'pandas', 'numpy', 'scikit-learn', 'sql', 'tableau', 'matplotlib', 'jupyter'],
    'machine learning': ['python', 'tensorflow', 'pytorch', 'scikit-learn', 'keras', 'numpy', 'pandas'],
    'devops': ['docker', 'kubernetes', 'jenkins', 'terraform', 'ansible', 'aws', 'ci/cd', 'linux'],
    'mobile': ['react native', 'flutter', 'swift', 'kotlin', 'android', 'ios', 'firebase'],
    'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'serverless', 'lambda'],
    'operations': ['asana', 'jira', 'trello', 'excel', 'google sheets', 'slack', 'process optimization', 'sop documentation'],
    'project management': ['asana', 'jira', 'trello', 'gantt charts', 'risk management', 'budget management', 'stakeholder communication'],
    
    # Tech domains - expanded
    'technical writing': ['markdown', 'confluence', 'swagger', 'gitbook', 'technical documentation', 'api documentation'],
    'qa testing': ['selenium', 'cypress', 'junit', 'pytest', 'test automation', 'postman', 'cucumber', 'testng'],
    'database administration': ['sql', 'oracle', 'postgresql', 'mysql', 'backup recovery', 'performance tuning', 'indexing'],
    'cybersecurity': ['penetration testing', 'owasp', 'firewalls', 'encryption', 'vulnerability assessment', 'network security'],
    'system administration': ['linux', 'bash', 'powershell', 'active directory', 'windows server', 'ssh', 'automation'],
    'game development': ['unity', 'c#', 'unreal engine', 'c++', '3d modeling', 'game design'],
    'embedded systems': ['c', 'c++', 'microcontrollers', 'arduino', 'rtos', 'raspberry pi', 'iot'],
    'blockchain': ['solidity', 'ethereum', 'smart contracts', 'web3', 'cryptocurrency', 'nft'],
    'data engineering': ['apache spark', 'airflow', 'kafka', 'etl', 'snowflake', 'data pipelines', 'sql'],
    'sre': ['prometheus', 'grafana', 'kubernetes', 'monitoring', 'incident management', 'alerting', 'oncall'],
    
    # Non-tech domains
    'hr recruitment': ['ats', 'linkedin recruiter', 'workday', 'bamboohr', 'recruitment', 'onboarding', 'talent acquisition'],
    'digital marketing': ['seo', 'google analytics', 'google ads', 'facebook ads', 'content marketing', 'mailchimp', 'hubspot'],
    'sales': ['salesforce', 'crm', 'pipedrive', 'cold calling', 'pipeline management', 'lead generation'],
    'customer support': ['zendesk', 'freshdesk', 'intercom', 'ticketing', 'customer success', 'help desk'],
    'finance accounting': ['quickbooks', 'sap', 'excel', 'financial modeling', 'gaap', 'budgeting', 'financial reporting'],
    'business analysis': ['requirements gathering', 'user stories', 'process mapping', 'sql', 'data analysis', 'visio'],
    'product management': ['roadmapping', 'product strategy', 'jira', 'user stories', 'mixpanel', 'amplitude', 'metrics'],
    'content writing': ['seo', 'wordpress', 'copywriting', 'content strategy', 'editing', 'cms']
}

SKILL_EXPLANATION_MAP = {
    'figma': 'Industry-standard collaborative design tool for UI/UX design, prototyping, and design systems',
    'sketch': 'Vector-based design tool for creating user interfaces and digital products',
    'adobe xd': 'Design and prototyping tool for creating wireframes, mockups, and interactive prototypes',
    'user research': 'Methods for understanding user behaviors, needs, and motivations through interviews and testing',
    'wireframing': 'Creating low-fidelity layouts to visualize structure and functionality before detailed design',
    'prototyping': 'Building interactive mockups to test and validate design concepts with users',
    'design systems': 'Comprehensive collection of reusable components, patterns, and guidelines for consistent design',
    'usability testing': 'Evaluating products by testing them with representative users to identify pain points',
    'interaction design': 'Designing interactive elements and user flows to create intuitive user experiences',
    'visual design': 'Creating aesthetically pleasing interfaces using typography, color, layout, and imagery',
    'accessibility': 'Designing products that are usable by people with diverse abilities and disabilities',
    'wcag': 'Web Content Accessibility Guidelines ensuring digital content is accessible to all users',
    'motion design': 'Creating animations and transitions to enhance user experience and provide visual feedback',
    'angular': 'Full-featured TypeScript framework for building scalable web applications',
    'vue': 'Progressive JavaScript framework for building user interfaces and single-page applications',
    'node.js': 'JavaScript runtime for building scalable server-side applications',
    'express': 'Minimalist web framework for Node.js, ideal for building APIs and web servers',
    'sql': 'Standard language for managing and querying relational databases',
    'laravel': 'PHP framework for building modern web applications with elegant syntax',
    'redux': 'State management library for React applications, essential for complex frontend architecture',
    'next.js': 'React framework for server-side rendering and static site generation',
    'typescript': 'Typed superset of JavaScript that improves code quality and maintainability',
    'docker': 'Containerization platform for packaging applications with dependencies',
    'kubernetes': 'Container orchestration system for deploying and scaling applications',
    'jwt': 'JSON Web Token standard for secure authentication and authorization',
    'rest api': 'Architectural style for designing networked applications using HTTP methods',
    'graphql': 'Query language for APIs providing flexible data fetching',
    'tensorflow': 'Open-source machine learning framework for training neural networks',
    'scikit-learn': 'Machine learning library for classification, regression, and clustering',
    'pandas': 'Data manipulation library essential for data analysis in Python',
    'numpy': 'Numerical computing library fundamental for scientific computing in Python',
    'postgresql': 'Advanced relational database with strong ACID compliance',
    'mongodb': 'NoSQL document database for flexible, scalable data storage',
    'angular': 'Full-featured TypeScript framework for building scalable web applications',
    'vue': 'Progressive JavaScript framework for building user interfaces and single-page applications',
    'django': 'High-level Python web framework for rapid development with clean, pragmatic design',
    'flask': 'Lightweight Python web framework for building APIs and web applications',
    'fastapi': 'Modern, fast Python framework for building APIs with automatic documentation',
    'aws': 'Amazon Web Services cloud platform for scalable infrastructure',
    'azure': 'Microsoft cloud computing platform for building, deploying, and managing applications',
    'gcp': 'Google Cloud Platform offering computing, storage, and machine learning services',
    'ci/cd': 'Continuous Integration and Deployment for automated testing and deployment',
    'unit testing': 'Testing methodology for validating individual components',
    'microservices': 'Architectural pattern for building distributed, scalable systems',
    'oauth': 'Authorization framework for secure third-party access',
    'webpack': 'Module bundler for JavaScript applications',
    'sass': 'CSS preprocessor adding variables and nesting for maintainable styles',
    'agile': 'Iterative development methodology emphasizing collaboration and flexibility',
    'jira': 'Project management and issue tracking tool widely used in agile teams',
    'asana': 'Work management platform for organizing tasks, projects, and team collaboration',
    'trello': 'Visual project management tool using kanban boards for task tracking',
    'confluence': 'Team collaboration and documentation platform for creating and sharing knowledge',
    'slack': 'Team communication platform for real-time messaging and collaboration',
    'microsoft teams': 'Collaboration platform integrating chat, meetings, and file sharing',
    'excel': 'Spreadsheet software for data analysis, reporting, and financial modeling',
    'google sheets': 'Cloud-based spreadsheet tool for collaborative data management and analysis',
    'power bi': 'Business analytics tool for visualizing data and sharing insights',
    'tableau': 'Data visualization software for creating interactive dashboards and reports',
    'project management': 'Discipline of planning, organizing, and managing resources to achieve specific goals',
    'sop documentation': 'Standard Operating Procedures for ensuring consistency and quality in operations',
    'process optimization': 'Systematic approach to improving efficiency and effectiveness of workflows',
    'git': 'Version control system for tracking code changes and collaboration',
    
    # Technical Writing & Documentation
    'markdown': 'Lightweight markup language for formatting text and creating documentation',
    'swagger': 'API documentation framework for designing, building, and documenting RESTful APIs',
    'openapi': 'API specification standard for describing REST APIs in machine-readable format',
    'technical writing': 'Creating clear technical documentation for software, hardware, and processes',
    'api documentation': 'Documentation describing how to use and integrate with APIs',
    'gitbook': 'Documentation platform for creating and hosting technical documentation',
    'docusaurus': 'Documentation website generator built with React for easy maintenance',
    'sphinx': 'Documentation generator for Python projects using reStructuredText',
    
    # QA & Testing
    'selenium': 'Browser automation framework for testing web applications across browsers',
    'cypress': 'Modern end-to-end testing framework for web applications with JavaScript',
    'junit': 'Unit testing framework for Java applications',
    'testng': 'Testing framework for Java inspired by JUnit with additional features',
    'test automation': 'Automated execution of software tests to improve efficiency and consistency',
    'postman': 'API development and testing tool for building, testing, and documenting APIs',
    'cucumber': 'Behavior-driven development (BDD) testing framework using Gherkin syntax',
    'bdd': 'Behavior-Driven Development approach focusing on collaboration and user behavior',
    'mockito': 'Java mocking framework for unit testing and test-driven development',
    
    # Database Administration
    'oracle': 'Enterprise relational database management system with advanced features',
    'database administration': 'Managing, maintaining, and optimizing database systems for performance',
    'backup recovery': 'Processes for backing up data and recovering from failures or disasters',
    'performance tuning': 'Optimizing database queries and configurations for better performance',
    'pl/sql': 'Oracle procedural language extension for SQL programming',
    'pgadmin': 'Administration and management tool for PostgreSQL databases',
    'redis': 'In-memory data structure store used as cache, database, and message broker',
    'nosql': 'Non-relational database approach for flexible, scalable data storage',
    
    # Security & Cybersecurity
    'cybersecurity': 'Practice of protecting systems, networks, and data from digital attacks',
    'penetration testing': 'Ethical hacking to identify security vulnerabilities before attackers do',
    'owasp': 'Open Web Application Security Project providing security best practices',
    'firewalls': 'Network security systems that monitor and control incoming/outgoing traffic',
    'encryption': 'Converting data into secure format to prevent unauthorized access',
    'vulnerability assessment': 'Identifying, quantifying, and prioritizing security vulnerabilities',
    'kali linux': 'Linux distribution designed for penetration testing and security auditing',
    'metasploit': 'Penetration testing framework for finding and exploiting vulnerabilities',
    'burp suite': 'Web application security testing toolkit for finding vulnerabilities',
    'siem': 'Security Information and Event Management for real-time security monitoring',
    
    # System Administration
    'linux': 'Open-source Unix-like operating system widely used in servers and development',
    'bash': 'Unix shell and command language for system administration and automation',
    'shell scripting': 'Writing scripts to automate system administration tasks',
    'powershell': 'Task automation and configuration management framework from Microsoft',
    'active directory': 'Microsoft directory service for Windows domain networks and authentication',
    'windows server': 'Microsoft server operating system for enterprise computing',
    'ssh': 'Secure Shell protocol for secure remote access to systems',
    'system administration': 'Managing and maintaining computer systems, servers, and networks',
    
    # Game Development
    'unity': 'Cross-platform game engine for creating 2D and 3D games',
    'c#': 'Modern object-oriented programming language developed by Microsoft',
    'unreal engine': 'Advanced game engine for creating high-fidelity gaming experiences',
    'game development': 'Process of designing, developing, and releasing video games',
    '3d modeling': 'Creating three-dimensional digital representations of objects',
    'blueprints': "Unreal Engine's visual scripting system for game logic without coding",
    
    # Embedded Systems
    'embedded systems': 'Computer systems integrated into devices to perform dedicated functions',
    'microcontrollers': 'Small computers on integrated circuits for embedded applications',
    'arduino': 'Open-source electronics platform for building digital devices and interactive objects',
    'rtos': 'Real-Time Operating System for applications requiring precise timing',
    'iot': 'Internet of Things - network of physical devices connected to the internet',
    'raspberry pi': 'Small single-board computer for learning programming and building projects',
    
    # Blockchain
    'blockchain': 'Distributed ledger technology for secure, transparent transactions',
    'solidity': 'Programming language for writing smart contracts on Ethereum blockchain',
    'ethereum': 'Decentralized blockchain platform for smart contracts and applications',
    'smart contracts': 'Self-executing contracts with terms directly written into code',
    'web3': 'Decentralized web built on blockchain technology',
    'cryptocurrency': 'Digital currency using cryptography for secure transactions',
    'metamask': 'Cryptocurrency wallet for interacting with Ethereum blockchain',
    
    # Data Engineering
    'apache spark': 'Unified analytics engine for large-scale data processing',
    'airflow': 'Platform for programmatically authoring, scheduling, and monitoring workflows',
    'kafka': 'Distributed streaming platform for building real-time data pipelines',
    'etl': 'Extract, Transform, Load process for data integration and warehousing',
    'snowflake': 'Cloud-based data warehousing platform for analytics',
    'data pipelines': 'Automated workflows for moving and transforming data between systems',
    'pyspark': 'Python API for Apache Spark for large-scale data processing',
    'hadoop': 'Framework for distributed storage and processing of big data',
    'big data': 'Extremely large datasets requiring specialized tools and techniques',
    
    # SRE & Monitoring
    'prometheus': 'Open-source monitoring system with time-series database',
    'grafana': 'Analytics and monitoring platform for visualizing metrics',
    'monitoring': 'Continuous observation of systems to ensure performance and availability',
    'alerting': 'Automated notifications for system issues and anomalies',
    'incident management': 'Process for responding to and resolving service disruptions',
    'oncall': 'On-call rotation for responding to system incidents',
    'sre': 'Site Reliability Engineering - ensuring reliable and scalable systems',
    'pagerduty': 'Incident management platform for alerting and on-call scheduling',
    'elasticsearch': 'Distributed search and analytics engine for log and data analysis',
    'kibana': 'Visualization tool for Elasticsearch data',
    'logstash': 'Data processing pipeline for ingesting and transforming logs',
    'elk stack': 'Elasticsearch, Logstash, Kibana stack for logging and monitoring',
    
    # HR & Recruitment
    'ats': 'Applicant Tracking System for managing recruitment and hiring processes',
    'linkedin recruiter': 'Tool for sourcing and contacting potential candidates on LinkedIn',
    'workday': 'Cloud-based human capital management and financial management software',
    'bamboohr': 'HR software for managing employee data, time tracking, and benefits',
    'recruitment': 'Process of finding, attracting, and hiring qualified candidates',
    'talent acquisition': 'Strategic approach to identifying and hiring skilled employees',
    'onboarding': 'Process of integrating new employees into the organization',
    'hris': 'Human Resource Information System for managing HR data and processes',
    
    # Digital Marketing
    'seo': 'Search Engine Optimization for improving website visibility in search results',
    'google analytics': 'Web analytics platform for tracking and reporting website traffic',
    'google ads': 'Online advertising platform for creating and managing paid ads',
    'ppc': 'Pay-Per-Click advertising model where advertisers pay for each ad click',
    'sem': 'Search Engine Marketing combining SEO and paid search advertising',
    'facebook ads': 'Facebook advertising platform for creating targeted ad campaigns',
    'social media marketing': 'Using social platforms to promote products and engage audiences',
    'mailchimp': 'Email marketing platform for creating and managing email campaigns',
    'hubspot': 'Inbound marketing and sales platform with CRM and automation',
    'content marketing': 'Creating valuable content to attract and engage target audiences',
    'copywriting': 'Writing persuasive marketing and advertising content',
    'keyword research': 'Identifying search terms people use to find information online',
    'email marketing': 'Using email to promote products and build relationships with customers',
    
    # Sales & CRM
    'salesforce': 'Leading cloud-based CRM platform for sales, service, and marketing',
    'crm': 'Customer Relationship Management system for managing customer interactions',
    'pipeline management': 'Tracking and managing sales opportunities through stages',
    'lead generation': 'Identifying and cultivating potential customers for sales',
    'pipedrive': 'Sales CRM tool designed to help manage leads and deals',
    'cold calling': 'Contacting potential customers who have not expressed interest',
    'sales automation': 'Using software to automate repetitive sales tasks',
    'apex': 'Salesforce proprietary programming language for custom development',
    
    # Customer Support
    'zendesk': 'Customer service platform for support ticket management',
    'freshdesk': 'Cloud-based customer support software for helpdesk management',
    'intercom': 'Customer messaging platform for support, engagement, and marketing',
    'customer support': 'Assistance provided to customers before, during, and after purchases',
    'ticketing': 'System for tracking and managing customer support requests',
    'help desk': 'Service providing information and support to users',
    'customer success': 'Ensuring customers achieve desired outcomes with products/services',
    'live chat': 'Real-time messaging for customer support on websites',
    
    # Finance & Accounting
    'quickbooks': 'Accounting software for small and medium-sized businesses',
    'sap': 'Enterprise Resource Planning software for business operations',
    'financial modeling': 'Creating representations of company financial performance',
    'gaap': 'Generally Accepted Accounting Principles for financial reporting',
    'accounting': 'Recording, classifying, and summarizing financial transactions',
    'bookkeeping': 'Recording daily financial transactions of a business',
    'financial reporting': 'Disclosing financial information to stakeholders',
    'budgeting': 'Planning and allocating financial resources',
    'forecasting': 'Predicting future financial outcomes based on data',
    'erp': 'Enterprise Resource Planning for integrated business management',
    
    # Business Analysis
    'business analysis': 'Identifying business needs and determining solutions',
    'requirements gathering': 'Collecting stakeholder needs and project requirements',
    'user stories': 'Short descriptions of features from user perspective',
    'process mapping': 'Visual documentation of business processes and workflows',
    'visio': 'Microsoft diagramming tool for creating flowcharts and diagrams',
    'stakeholder management': 'Engaging and managing relationships with project stakeholders',
    'bpmn': 'Business Process Model and Notation for process documentation',
    
    # Product Management
    'product management': 'Guiding product development from conception to launch',
    'roadmapping': 'Creating strategic plan for product features and timeline',
    'product strategy': 'Long-term plan for product development and market positioning',
    'mixpanel': 'Product analytics platform for tracking user behavior',
    'amplitude': 'Digital analytics platform for understanding product usage',
    'product analytics': 'Analyzing user interactions to improve product decisions',
    'a/b testing': 'Comparing two versions to determine which performs better',
    'metrics': 'Quantitative measures for tracking performance and success',
    'market research': 'Gathering information about target markets and customers',
    
    # Content Writing
    'wordpress': 'Content management system for creating websites and blogs',
    'cms': 'Content Management System for creating and managing digital content',
    'content strategy': 'Planning creation, delivery, and governance of content',
    'editing': 'Reviewing and refining written content for clarity and accuracy',
    'blogging': 'Writing and publishing articles on websites or platforms'
}

def normalize_skill(skill: str) -> str:
    if not skill:
        return ""
    return skill.lower().strip()

def suggest_skills_by_co_occurrence(jd_skills: List[str], resume_skills: List[str], detected_domain: str = None) -> List[Dict[str, str]]:
    jd_normalized = set(normalize_skill(s) for s in jd_skills)
    resume_normalized = set(normalize_skill(s) for s in resume_skills)
    
    # Define irrelevant skills by domain to filter out
    domain_exclusions = {
        # Development domains - exclude data science/ML
        'web development': ['numpy', 'pandas', 'scikit-learn', 'tensorflow', 'pytorch', 'matplotlib', 'seaborn', 'jupyter'],
        'frontend': ['numpy', 'pandas', 'scikit-learn', 'tensorflow', 'pytorch', 'matplotlib', 'seaborn', 'jupyter', 'django', 'flask', 'spring boot'],
        'backend': ['numpy', 'pandas', 'scikit-learn', 'tensorflow', 'pytorch', 'matplotlib', 'seaborn', 'jupyter', 'react', 'angular', 'vue', 'figma', 'sketch'],
        'fullstack': ['numpy', 'pandas', 'scikit-learn', 'tensorflow', 'pytorch', 'matplotlib', 'seaborn', 'jupyter'],
        'mobile': ['django', 'flask', 'spring boot', 'react', 'angular', 'vue', 'pandas', 'numpy', 'scikit-learn'],
        
        # Design domains - exclude development frameworks
        'ui/ux': ['django', 'flask', 'spring boot', 'pandas', 'numpy', 'webpack', 'babel', 'kubernetes', 'docker', 'terraform'],
        'design': ['django', 'flask', 'spring boot', 'pandas', 'numpy', 'webpack', 'babel', 'kubernetes', 'docker'],
        
        # Data/ML domains - exclude web frameworks
        'data science': ['react', 'angular', 'vue', 'django', 'flask', 'spring boot', 'node.js', 'express', 'figma', 'sketch'],
        'machine learning': ['react', 'angular', 'vue', 'django', 'flask', 'spring boot', 'node.js', 'express', 'figma', 'sketch'],
        'data engineering': ['react', 'angular', 'vue', 'figma', 'sketch', 'adobe xd', 'prototyping'],
        
        # Infrastructure domains - exclude web/design
        'devops': ['react', 'angular', 'vue', 'figma', 'sketch', 'pandas', 'numpy', 'scikit-learn', 'tensorflow'],
        'sre': ['react', 'angular', 'vue', 'figma', 'sketch', 'pandas', 'numpy', 'scikit-learn'],
        'cloud': ['react', 'angular', 'vue', 'figma', 'sketch', 'pandas', 'numpy', 'scikit-learn'],
        'system administration': ['react', 'angular', 'vue', 'figma', 'sketch', 'pandas', 'numpy', 'tensorflow', 'django', 'flask'],
        
        # Technical specialist domains
        'qa testing': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'figma', 'sketch', 'adobe xd'],
        'database administration': ['react', 'angular', 'vue', 'figma', 'sketch', 'pandas', 'numpy', 'tensorflow', 'pytorch'],
        'cybersecurity': ['react', 'angular', 'vue', 'figma', 'sketch', 'pandas', 'numpy', 'tensorflow', 'django', 'flask'],
        'technical writing': ['react', 'angular', 'vue', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'kubernetes', 'docker'],
        
        # Specialized development
        'game development': ['react', 'angular', 'vue', 'django', 'flask', 'pandas', 'numpy', 'scikit-learn', 'kubernetes'],
        'embedded systems': ['react', 'angular', 'vue', 'django', 'flask', 'pandas', 'numpy', 'kubernetes', 'figma'],
        'blockchain': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'figma', 'sketch'],
        
        # Business/Operations domains - exclude ALL technical development
        'operations': ['django', 'flask', 'spring boot', 'react', 'angular', 'vue', 'node.js', 'numpy', 'pandas', 'scikit-learn', 'tensorflow', 'pytorch', 'docker', 'kubernetes', 'webpack', 'babel', 'c++', 'java', 'python'],
        'project management': ['django', 'flask', 'spring boot', 'react', 'angular', 'vue', 'node.js', 'numpy', 'pandas', 'scikit-learn', 'tensorflow', 'pytorch', 'docker', 'kubernetes', 'webpack', 'babel', 'c++', 'java'],
        'product management': ['django', 'flask', 'spring boot', 'numpy', 'pandas', 'scikit-learn', 'tensorflow', 'pytorch', 'docker', 'kubernetes', 'c++'],
        'hr recruitment': ['django', 'flask', 'react', 'angular', 'vue', 'numpy', 'pandas', 'scikit-learn', 'tensorflow', 'docker', 'kubernetes', 'c++', 'java', 'python', 'javascript'],
        'digital marketing': ['django', 'flask', 'react', 'angular', 'vue', 'numpy', 'pandas', 'scikit-learn', 'tensorflow', 'docker', 'kubernetes', 'c++', 'java', 'python'],
        'sales': ['django', 'flask', 'react', 'angular', 'vue', 'numpy', 'pandas', 'scikit-learn', 'tensorflow', 'docker', 'kubernetes', 'c++', 'java', 'python', 'javascript'],
        'customer support': ['django', 'flask', 'react', 'angular', 'vue', 'numpy', 'pandas', 'scikit-learn', 'tensorflow', 'docker', 'kubernetes', 'c++', 'java', 'python'],
        'finance accounting': ['django', 'flask', 'react', 'angular', 'vue', 'numpy', 'pandas', 'scikit-learn', 'tensorflow', 'docker', 'kubernetes', 'c++', 'figma'],
        'business analysis': ['react', 'angular', 'vue', 'numpy', 'pandas', 'scikit-learn', 'tensorflow', 'docker', 'kubernetes', 'c++', 'figma', 'sketch'],
        'content writing': ['django', 'flask', 'react', 'angular', 'vue', 'numpy', 'pandas', 'scikit-learn', 'tensorflow', 'docker', 'kubernetes', 'c++', 'java', 'python'],
    }
    
    # For generic roles (no detected domain), only suggest broadly applicable tools
    # Exclude domain-specific frameworks/libraries
    general_allowed_skills = ['git', 'docker', 'kubernetes', 'ci/cd', 'agile', 'unit testing', 
                               'rest api', 'sql', 'postgresql', 'mysql', 'mongodb', 'redis',
                               'aws', 'azure', 'gcp', 'linux', 'bash']
    
    excluded_skills = set()
    if detected_domain and detected_domain in domain_exclusions:
        excluded_skills = set(normalize_skill(s) for s in domain_exclusions[detected_domain])
    elif not detected_domain:
        # No domain detected - be conservative, only suggest general tools
        # Exclude web frameworks, ML libraries, and specialized tools
        excluded_skills = set(normalize_skill(s) for s in [
            'django', 'flask', 'fastapi', 'spring boot', 'laravel',
            'react', 'angular', 'vue', 'next.js', 'svelte',
            'numpy', 'pandas', 'scikit-learn', 'tensorflow', 'pytorch', 'matplotlib', 'seaborn', 'jupyter',
            'webpack', 'babel', 'sass', 'less',
            'figma', 'sketch', 'adobe xd'
        ])
    
    suggestions = []
    seen = set()
    
    for jd_skill in jd_normalized:
        if jd_skill in SKILL_CO_OCCURRENCE_MAP:
            related_skills = SKILL_CO_OCCURRENCE_MAP[jd_skill]
            for related in related_skills:
                related_norm = normalize_skill(related)
                # Skip if already in resume, already suggested, or excluded for this domain
                if related_norm not in resume_normalized and related_norm not in seen and related_norm not in excluded_skills:
                    seen.add(related_norm)
                    explanation = SKILL_EXPLANATION_MAP.get(related_norm, f"Commonly used with {jd_skill}")
                    
                    # Only mark as high priority if domain-specific context OR universally important
                    is_universal = related_norm in ['docker', 'git', 'ci/cd', 'unit testing', 'agile']
                    is_high = is_universal or (detected_domain and related_norm in ['rest api', 'sql', 'mongodb', 'postgresql'])
                    
                    suggestions.append({
                        'skill': related,
                        'reason': f"Recommended for {jd_skill}",
                        'explanation': explanation,
                        'priority': 'high' if is_high else 'medium'
                    })
    
    return suggestions[:15]

def suggest_skills_by_domain(job_role: str, jd_text: str, resume_skills: List[str]) -> List[Dict[str, str]]:
    text_lower = normalize_skill(job_role + ' ' + jd_text)
    job_role_lower = normalize_skill(job_role)
    resume_normalized = set(normalize_skill(s) for s in resume_skills)
    
    detected_domain = None
    
    # Step 1: Check for DEVELOPER/ENGINEER roles FIRST (these mention design but aren't design roles)
    # Step 1: Check for OPERATIONS/BUSINESS roles first (highest priority for non-technical)
    operations_roles = ['operations coordinator', 'operations manager', 'project coordinator', 
                        'administrative', 'office manager', 'business operations']
    if any(role in job_role_lower for role in operations_roles):
        detected_domain = 'operations'
    
    # Step 2: Check for PROJECT MANAGEMENT roles
    elif 'project manager' in job_role_lower or 'program manager' in job_role_lower or 'pmo' in job_role_lower:
        detected_domain = 'project management'
    
    # Step 3: Check for PRODUCT MANAGEMENT roles
    elif 'product manager' in job_role_lower or 'product owner' in job_role_lower:
        detected_domain = 'product management'
    
    # Step 4: Check for NON-TECHNICAL roles
    elif 'recruiter' in job_role_lower or 'talent acquisition' in job_role_lower or 'hr' in job_role_lower:
        detected_domain = 'hr recruitment'
    elif any(role in job_role_lower for role in ['marketing', 'seo specialist', 'digital marketer', 'content marketer']):
        detected_domain = 'digital marketing'
    elif 'sales' in job_role_lower or 'account executive' in job_role_lower or 'business development' in job_role_lower:
        detected_domain = 'sales'
    elif any(role in job_role_lower for role in ['customer support', 'customer success', 'support engineer', 'help desk']):
        detected_domain = 'customer support'
    elif any(role in job_role_lower for role in ['accountant', 'financial analyst', 'finance', 'bookkeeper']):
        detected_domain = 'finance accounting'
    elif 'business analyst' in job_role_lower or 'ba' in job_role_lower:
        detected_domain = 'business analysis'
    elif any(role in job_role_lower for role in ['content writer', 'copywriter', 'technical writer', 'writer']):
        # Check if it's technical writer
        if 'technical' in job_role_lower or 'api' in text_lower or 'documentation' in text_lower:
            detected_domain = 'technical writing'
        else:
            detected_domain = 'content writing'
    
    # Step 5: Check for TECHNICAL SPECIALIST roles
    elif any(role in job_role_lower for role in ['qa', 'quality assurance', 'test engineer', 'sdet', 'automation tester']):
        detected_domain = 'qa testing'
    elif any(role in job_role_lower for role in ['dba', 'database administrator', 'database engineer']):
        detected_domain = 'database administration'
    elif any(role in job_role_lower for role in ['security engineer', 'cybersecurity', 'infosec', 'penetration tester']):
        detected_domain = 'cybersecurity'
    elif any(role in job_role_lower for role in ['system administrator', 'sysadmin', 'systems engineer', 'infrastructure']):
        detected_domain = 'system administration'
    elif any (role in job_role_lower for role in ['devops', 'site reliability', 'sre', 'platform engineer']):
        if 'sre' in job_role_lower or 'site reliability' in job_role_lower:
            detected_domain = 'sre'
        else:
            detected_domain = 'devops'
    elif any(role in job_role_lower for role in ['data engineer', 'etl developer', 'big data']):
        detected_domain = 'data engineering'
    elif any(role in job_role_lower for role in ['data scientist', 'ml engineer', 'machine learning']):
        if 'machine learning' in job_role_lower or 'ml engineer' in job_role_lower:
            detected_domain = 'machine learning'
        else:
            detected_domain = 'data science'
    elif any(role in job_role_lower for role in ['game developer', 'game programmer', 'game designer']):
        detected_domain = 'game development'
    elif any(role in job_role_lower for role in ['embedded', 'firmware', 'iot engineer']):
        detected_domain = 'embedded systems'
    elif any(role in job_role_lower for role in ['blockchain', 'smart contract', 'web3']):
        detected_domain = 'blockchain'
    elif any(role in job_role_lower for role in ['cloud engineer', 'cloud architect', 'aws', 'azure', 'gcp']):
        detected_domain = 'cloud'
    elif any(role in job_role_lower for role in ['mobile developer', 'ios developer', 'android developer']):
        detected_domain = 'mobile'
    
    # Step 6: Check for DEVELOPMENT roles
    elif 'web developer' in job_role_lower or ('web development' in job_role_lower and 'html' in text_lower and 'css' in text_lower):
        detected_domain = 'web development'
    elif 'frontend' in job_role_lower or 'front end' in job_role_lower:
        detected_domain = 'frontend'
    elif 'backend' in job_role_lower or 'back end' in job_role_lower:
        detected_domain = 'backend'
    elif 'fullstack' in job_role_lower or 'full stack' in job_role_lower:
        detected_domain = 'fullstack'
    
    # Step 7: Check for DESIGN roles
    elif any(role in job_role_lower for role in ['ui ux designer', 'ux ui designer', 'product designer', 
                                                   'interaction designer', 'visual designer', 'ui designer', 
                                                   'ux designer', 'graphic designer']):
        # Check if it's genuinely a design role with design tools mentioned
        design_tool_count = sum(1 for tool in ['figma', 'sketch', 'adobe xd', 'wireframe', 'prototype'] if tool in text_lower)
        if design_tool_count >= 1:
            detected_domain = 'ui/ux'
        else:
            detected_domain = 'design'
    
    # Step 8: Fall back to keyword matching for other domains
    else:
        for domain, keywords in DOMAIN_SKILL_MAP.items():
            excluded_from_fallback = ['ui/ux', 'design', 'web development', 'operations', 'project management',
                                      'product management', 'hr recruitment', 'digital marketing', 'sales',
                                      'customer support', 'finance accounting', 'business analysis', 'content writing',
                                      'technical writing', 'qa testing', 'database administration', 'cybersecurity',
                                      'system administration', 'sre', 'devops', 'data engineering', 'game development',
                                      'embedded systems', 'blockchain', 'cloud', 'mobile']
            if domain in excluded_from_fallback:
                continue  # Already checked these
            if any(normalize_skill(keyword) in text_lower for keyword in keywords[:3]):
                detected_domain = domain
                break
    
    if not detected_domain:
        return []
    
    suggestions = []
    domain_skills = DOMAIN_SKILL_MAP.get(detected_domain, [])
    
    for skill in domain_skills:
        skill_norm = normalize_skill(skill)
        if skill_norm not in resume_normalized:
            explanation = SKILL_EXPLANATION_MAP.get(skill_norm, f"Core skill for {detected_domain} development")
            suggestions.append({
                'skill': skill,
                'reason': f"Essential for {detected_domain} role",
                'explanation': explanation,
                'priority': 'high'
            })
    
    return suggestions[:10]

def get_skill_explanation(skill: str) -> str:
    skill_norm = normalize_skill(skill)
    return SKILL_EXPLANATION_MAP.get(skill_norm, f"{skill} is a required technical skill for this position")

def generate_skill_suggestions(
    jd_skills: List[str],
    resume_skills: List[str],
    job_role: str = "",
    jd_text: str = "",
    missing_skills: List[str] = None
) -> Dict[str, any]:
    
    # First detect domain for context-aware recommendations
    text_lower = normalize_skill(job_role + ' ' + jd_text)
    job_role_lower = normalize_skill(job_role)
    detected_domain = None
    
    # Domain detection - prioritize non-technical roles first (must match suggest_skills_by_domain logic)
    operations_roles = ['operations coordinator', 'operations manager', 'project coordinator', 
                        'administrative', 'office manager', 'business operations']
    if any(role in job_role_lower for role in operations_roles):
        detected_domain = 'operations'
    elif 'project manager' in job_role_lower or 'program manager' in job_role_lower or 'pmo' in job_role_lower:
        detected_domain = 'project management'
    elif 'product manager' in job_role_lower or 'product owner' in job_role_lower:
        detected_domain = 'product management'
    elif 'recruiter' in job_role_lower or 'talent acquisition' in job_role_lower or 'hr' in job_role_lower:
        detected_domain = 'hr recruitment'
    elif any(role in job_role_lower for role in ['marketing', 'seo specialist', 'digital marketer', 'content marketer']):
        detected_domain = 'digital marketing'
    elif 'sales' in job_role_lower or 'account executive' in job_role_lower or 'business development' in job_role_lower:
        detected_domain = 'sales'
    elif any(role in job_role_lower for role in ['customer support', 'customer success', 'support engineer', 'help desk']):
        detected_domain = 'customer support'
    elif any(role in job_role_lower for role in ['accountant', 'financial analyst', 'finance', 'bookkeeper']):
        detected_domain = 'finance accounting'
    elif 'business analyst' in job_role_lower or 'ba' in job_role_lower:
        detected_domain = 'business analysis'
    elif any(role in job_role_lower for role in ['content writer', 'copywriter', 'technical writer', 'writer']):
        if 'technical' in job_role_lower or 'api' in text_lower or 'documentation' in text_lower:
            detected_domain = 'technical writing'
        else:
            detected_domain = 'content writing'
    elif any(role in job_role_lower for role in ['qa', 'quality assurance', 'test engineer', 'sdet', 'automation tester']):
        detected_domain = 'qa testing'
    elif any(role in job_role_lower for role in ['dba', 'database administrator', 'database engineer']):
        detected_domain = 'database administration'
    elif any(role in job_role_lower for role in ['security engineer', 'cybersecurity', 'infosec', 'penetration tester']):
        detected_domain = 'cybersecurity'
    elif any(role in job_role_lower for role in ['system administrator', 'sysadmin', 'systems engineer', 'infrastructure']):
        detected_domain = 'system administration'
    elif any(role in job_role_lower for role in ['devops', 'site reliability', 'sre', 'platform engineer']):
        if 'sre' in job_role_lower or 'site reliability' in job_role_lower:
            detected_domain = 'sre'
        else:
            detected_domain = 'devops'
    elif any(role in job_role_lower for role in ['data engineer', 'etl developer', 'big data']):
        detected_domain = 'data engineering'
    elif any(role in job_role_lower for role in ['data scientist', 'ml engineer', 'machine learning']):
        if 'machine learning' in job_role_lower or 'ml engineer' in job_role_lower:
            detected_domain = 'machine learning'
        else:
            detected_domain = 'data science'
    elif any(role in job_role_lower for role in ['game developer', 'game programmer', 'game designer']):
        detected_domain = 'game development'
    elif any(role in job_role_lower for role in ['embedded', 'firmware', 'iot engineer']):
        detected_domain = 'embedded systems'
    elif any(role in job_role_lower for role in ['blockchain', 'smart contract', 'web3']):
        detected_domain = 'blockchain'
    elif any(role in job_role_lower for role in ['cloud engineer', 'cloud architect', 'aws', 'azure', 'gcp']):
        detected_domain = 'cloud'
    elif any(role in job_role_lower for role in ['mobile developer', 'ios developer', 'android developer']):
        detected_domain = 'mobile'
    elif 'web developer' in job_role_lower or ('web development' in job_role_lower and 'html' in text_lower and 'css' in text_lower):
        detected_domain = 'web development'
    elif 'frontend' in job_role_lower or 'front end' in job_role_lower:
        detected_domain = 'frontend'
    elif 'backend' in job_role_lower or 'back end' in job_role_lower:
        detected_domain = 'backend'
    elif 'fullstack' in job_role_lower or 'full stack' in job_role_lower:
        detected_domain = 'fullstack'
    elif any(role in job_role_lower for role in ['ui ux designer', 'ux ui designer', 'product designer', 'ui designer', 'ux designer']):
        detected_domain = 'ui/ux'
    
    co_occurrence_suggestions = suggest_skills_by_co_occurrence(jd_skills, resume_skills, detected_domain)
    domain_suggestions = suggest_skills_by_domain(job_role, jd_text, resume_skills)
    
    # Prioritize missing skills from JD as HIGH priority
    missing_skill_suggestions = []
    if missing_skills:
        resume_normalized = set(normalize_skill(s) for s in resume_skills)
        for skill in missing_skills[:8]:  # Top 8 missing skills
            skill_norm = normalize_skill(skill)
            if skill_norm not in resume_normalized:
                explanation = get_skill_explanation(skill)
                missing_skill_suggestions.append({
                    'skill': skill,
                    'reason': f"Required in job description",
                    'explanation': explanation,
                    'priority': 'high'
                })
    
    all_suggestions = missing_skill_suggestions + co_occurrence_suggestions + domain_suggestions
    
    seen_skills = set()
    unique_suggestions = []
    for sug in all_suggestions:
        skill_norm = normalize_skill(sug['skill'])
        if skill_norm not in seen_skills:
            seen_skills.add(skill_norm)
            unique_suggestions.append(sug)
    
    unique_suggestions.sort(key=lambda x: (x['priority'] == 'high', x['skill']), reverse=True)
    
    missing_with_explanations = []
    if missing_skills:
        for skill in missing_skills[:20]:
            missing_with_explanations.append({
                'skill': skill,
                'explanation': get_skill_explanation(skill),
                'status': 'required'
            })
    
    return {
        'suggested_skills': unique_suggestions[:12],
        'missing_skills_explained': missing_with_explanations,
        'total_suggestions': len(unique_suggestions),
        'suggestion_categories': {
            'co_occurrence': len(co_occurrence_suggestions),
            'domain_based': len(domain_suggestions)
        }
    }

def get_learning_resources(skills: List[str]) -> Dict[str, List[str]]:
    resource_map = {
        'react': ['React Official Docs', 'freeCodeCamp React Course', 'React Tutorial for Beginners'],
        'python': ['Python.org Tutorial', 'Automate the Boring Stuff', 'Python for Data Science'],
        'docker': ['Docker Official Tutorial', 'Docker for Beginners', 'Docker Mastery Course'],
        'kubernetes': ['Kubernetes Official Docs', 'Kubernetes Basics', 'CKA Certification Prep'],
        'aws': ['AWS Free Tier', 'AWS Solutions Architect Associate', 'AWS Fundamentals'],
        'machine learning': ['Coursera ML by Andrew Ng', 'Fast.ai', 'Google ML Crash Course']
    }
    
    resources = {}
    for skill in skills[:5]:
        skill_norm = normalize_skill(skill)
        if skill_norm in resource_map:
            resources[skill] = resource_map[skill_norm]
    
    return resources

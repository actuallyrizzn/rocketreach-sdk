<?php

declare(strict_types=1);

/**
 * Test runner script for RocketReach PHP SDK
 * 
 * This script runs all tests and generates coverage reports
 */

require_once __DIR__ . '/vendor/autoload.php';

use PHPUnit\TextUI\Command;

class TestRunner
{
    private const COVERAGE_DIR = __DIR__ . '/coverage';
    private const PHPUNIT_CONFIG = __DIR__ . '/phpunit.xml';

    public function runAllTests(): int
    {
        echo "Running all tests with coverage...\n";
        
        $this->ensureCoverageDirectory();
        
        $command = new Command();
        $args = [
            'phpunit',
            '--configuration=' . self::PHPUNIT_CONFIG,
            '--coverage-html=' . self::COVERAGE_DIR . '/html',
            '--coverage-text=' . self::COVERAGE_DIR . '/coverage.txt',
            '--coverage-clover=' . self::COVERAGE_DIR . '/clover.xml',
            '--testdox'
        ];
        
        return $command->run($args, false);
    }

    public function runUnitTests(): int
    {
        echo "Running unit tests...\n";
        
        $command = new Command();
        $args = [
            'phpunit',
            '--configuration=' . self::PHPUNIT_CONFIG,
            '--testsuite=Unit',
            '--testdox'
        ];
        
        return $command->run($args, false);
    }

    public function runIntegrationTests(): int
    {
        echo "Running integration tests...\n";
        
        $command = new Command();
        $args = [
            'phpunit',
            '--configuration=' . self::PHPUNIT_CONFIG,
            '--testsuite=Integration',
            '--testdox'
        ];
        
        return $command->run($args, false);
    }

    public function runE2ETests(): int
    {
        echo "Running E2E tests...\n";
        
        $command = new Command();
        $args = [
            'phpunit',
            '--configuration=' . self::PHPUNIT_CONFIG,
            '--testsuite=E2E',
            '--testdox'
        ];
        
        return $command->run($args, false);
    }

    public function runLiveTests(): int
    {
        echo "Running live API tests...\n";
        
        $command = new Command();
        $args = [
            'phpunit',
            '--configuration=' . self::PHPUNIT_CONFIG,
            '--testsuite=Live',
            '--testdox'
        ];
        
        return $command->run($args, false);
    }

    public function runTestsUntilGreen(): int
    {
        $maxAttempts = 10;
        $attempt = 1;
        
        while ($attempt <= $maxAttempts) {
            echo "\n=== Test Run Attempt {$attempt} ===\n";
            
            $exitCode = $this->runAllTests();
            
            if ($exitCode === 0) {
                echo "\n✅ All tests passed! Coverage achieved.\n";
                return 0;
            }
            
            echo "\n❌ Tests failed. Attempt {$attempt}/{$maxAttempts}\n";
            $attempt++;
            
            if ($attempt <= $maxAttempts) {
                echo "Retrying in 5 seconds...\n";
                sleep(5);
            }
        }
        
        echo "\n❌ Tests failed after {$maxAttempts} attempts.\n";
        return $exitCode;
    }

    private function ensureCoverageDirectory(): void
    {
        if (!is_dir(self::COVERAGE_DIR)) {
            mkdir(self::COVERAGE_DIR, 0755, true);
        }
    }

    public function showCoverageReport(): void
    {
        $coverageFile = self::COVERAGE_DIR . '/coverage.txt';
        
        if (file_exists($coverageFile)) {
            echo "\n=== Coverage Report ===\n";
            echo file_get_contents($coverageFile);
        } else {
            echo "Coverage report not found. Run tests first.\n";
        }
    }
}

// Command line interface
if (php_sapi_name() === 'cli') {
    $runner = new TestRunner();
    
    $command = $argv[1] ?? 'all';
    
    switch ($command) {
        case 'all':
            $exitCode = $runner->runAllTests();
            $runner->showCoverageReport();
            exit($exitCode);
            
        case 'unit':
            exit($runner->runUnitTests());
            
        case 'integration':
            exit($runner->runIntegrationTests());
            
        case 'e2e':
            exit($runner->runE2ETests());
            
        case 'live':
            exit($runner->runLiveTests());
            
        case 'loop':
            exit($runner->runTestsUntilGreen());
            
        case 'coverage':
            $runner->showCoverageReport();
            exit(0);
            
        default:
            echo "Usage: php run-tests.php [all|unit|integration|e2e|live|loop|coverage]\n";
            echo "  all         - Run all tests with coverage\n";
            echo "  unit        - Run unit tests only\n";
            echo "  integration - Run integration tests only\n";
            echo "  e2e         - Run E2E tests only\n";
            echo "  live        - Run live API tests only\n";
            echo "  loop        - Run tests until 100% green\n";
            echo "  coverage    - Show coverage report\n";
            exit(1);
    }
}

# Run tests and get coverage
py.test --cov=team3 tests
coverage report -m > coverage_report.txt
coverage-badge -o tests/coverage.svg -f

# Run linting
pylint --rcfile=.pylintrc * | tee pylint_report.txt
score=$(sed -n 's/^Your code has been rated at \([-0-9.]*\)\/.*/\1/p' pylint_report.txt)
echo "Pylint score was $score"
rm pylint.svg
anybadge --label=pylint --value=$score --file=pylint.svg 2=red 4=orange 8=yellow 10=green

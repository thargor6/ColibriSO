package com.overwhale.colibri_so.frontend.service;

import com.overwhale.colibri_so.backend.entity.SnippetProject;
import com.overwhale.colibri_so.backend.repository.SnippetProjectRepository;
import com.overwhale.colibri_so.frontend.dto.SnippetProjectDto;
import com.overwhale.colibri_so.frontend.mapper.SnippetProjectMapper;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Service;
import org.vaadin.artur.helpers.CrudService;

import java.util.Optional;
import java.util.UUID;

@Service
public class SnippetProjectService extends CrudService<SnippetProjectDto, UUID> {
  private final SnippetProjectRepository repository;
  private final SnippetProjectMapper snippetProjectMapper;

  public SnippetProjectService(SnippetProjectRepository repository, SnippetProjectMapper snippetProjectMapper) {
    this.repository = repository;
    this.snippetProjectMapper = snippetProjectMapper;
  }

  public SnippetProjectDto update(SnippetProjectDto dto) {
    SnippetProject entity = snippetProjectMapper.dtoToEntiy(dto);
    return snippetProjectMapper.entityToDto(repository.save(entity));
  }

  @Override
  protected JpaRepository<SnippetProjectDto, UUID> getRepository() {
    return null;
  }

  public Optional<SnippetProjectDto> get(UUID id) {
    return repository.findById(id).map(e -> snippetProjectMapper.entityToDto(e));
  }

  public void delete(UUID id) {
    repository.deleteById(id);
  }

  public Page<SnippetProjectDto> list(Pageable pageable) {
    return repository.findAll(pageable).map(e -> snippetProjectMapper.entityToDto(e));
  }

  public int count() {
    return (int) repository.count();
  }
}
